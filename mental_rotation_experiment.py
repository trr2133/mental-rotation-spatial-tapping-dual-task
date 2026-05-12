import random
import pandas as pd
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim
from psychopy.core import Clock, quit, wait
from psychopy.hardware.keyboard import Keyboard

#PARAMETERS
angles = [0, 50, 100, 150]
tap_keys_right_handers = ['z', 'x', 'c', 'v']
tap_keys_left_handers  = ['m', ',', '.', '/']
n_practice = 8
n_trials_per_angle = 20
fixation_dur = 0.5
max_rt = 10.0
feedback_dur = 0.5

#PARTICIPANT INFO
exp_info = {'Participant ID': '', 'Age': '', 'Gender': ['Prefer not to say', 'Female', 'Male', 'Non-binary', 'Other'], 'Handedness': ['Right', 'Left']}
dlg = DlgFromDict(exp_info, title='Mental Rotation Experiment', order=['Participant ID', 'Age', 'Gender', 'Handedness'])
if not dlg.OK:
    quit()

#ASSIGN TAPPING HAND BASED ON HANDEDNESS
if exp_info['Handedness'] == 'Left':
    tap_keys = tap_keys_left_handers
    tapping_hand = 'right'
else:
    tap_keys = tap_keys_right_handers
    tapping_hand = 'left'

win = Window(size=[1024, 768], color='black', units='pix', fullscr=False)
kb = Keyboard()

#LOAD STIMULI
trial_pool = pd.read_csv('trials.csv')

#BUILD BLOCK SEQUENCE
def build_block(condition, n_per_angle):
    block = []
    for angle in angles:
        same = trial_pool[(trial_pool['angle'] == angle) & (trial_pool['trial_type'] == 'same')]
        diff = trial_pool[(trial_pool['angle'] == angle) & (trial_pool['trial_type'] == 'different')]
        selected = pd.concat([same.sample(n=n_per_angle // 2, replace=False),
                              diff.sample(n=n_per_angle - n_per_angle // 2, replace=False)])
        selected = selected.copy()
        selected['condition'] = condition
        block.append(selected)
    block = pd.concat(block).sample(frac=1).reset_index(drop=True)
    return block

#VISUAL STIMULI
fixation      = TextStim(win, text='+', color='white', height=40)
prompt        = TextStim(win, text='Same (F)   or   Different (J)?', color='white', height=24, pos=[0, -200])
tap_reminder  = TextStim(win, text=f"TAP: {' -> '.join(k.upper() for k in tap_keys)} (repeat, ~1 per second)", color=[1, 0.85, 0], height=22, pos=[0, 220])
tap_indicator = TextStim(win, text='', color=[0.4, 1, 0.4], height=24, pos=[0, 190])
msg           = TextStim(win, text='', color='white', height=24, wrapWidth=850, alignText='center')
fb_correct    = TextStim(win, text='Correct!',  color=[0.2, 1, 0.2], height=36)
fb_incorrect  = TextStim(win, text='Incorrect', color=[1, 0.2, 0.2], height=36)
fb_timeout    = TextStim(win, text='Too slow!', color=[1, 0.6, 0],   height=36)
stimulus_img  = ImageStim(win, pos=[0, 30], size=[None, 340])

def wait_for_space():
    kb.clearEvents()
    while True:
        keys = kb.getKeys(keyList=['space'], waitRelease=False)
        if 'space' in keys:
            break

msg.text = """Welcome to the Mental Rotation Experiment!

On each trial you will see two 3D shapes side by side.

Press F if the shapes are the SAME object (just rotated).
Press J if the shapes are DIFFERENT (one is a mirror image).

Respond as quickly and accuratelt as possible.
There is a 10-second time limit per trial.

You will first complete a short practice block with feedback.

Press SPACE to begin practice."""
msg.draw()
win.flip()
wait_for_space()

#RUNNING EXPERIMENT
alldata = []

# Counterbalance single-task and dual-task block order across participants
block_order = ['single', 'dual']
random.shuffle(block_order)

# Practice first, then the two main blocks
blocks_to_run = [('practice', True)] + [(c, False) for c in block_order]

for block_n, (condition, give_feedback) in enumerate(blocks_to_run):

    if condition == 'practice':
        trials = build_block('practice', max(1, n_practice // len(angles)))
    else:
        if condition == 'dual':
            msg.text = f"""DUAL-TASK BLOCK

This block adds a TAPPING task.

While judging the shapes, tap this sequence with your {tapping_hand} (non-dominant) hand,
roughly once per second:

        {' -> '.join(k.upper() for k in tap_keys)} -> ...

The screen will show which key to press next.

Try your best at BOTH tasks. Do not sacrifice one for the other.

Press SPACE to begin."""
        else:
            msg.text = """BLOCK: Mental Rotation ONLY

F = SAME    J = DIFFERENT

Press SPACE to begin."""
        msg.draw()
        win.flip()
        wait_for_space()
        trials = build_block(condition, n_trials_per_angle)

    block_correct = 0

    for trial_n, trial in trials.iterrows():

        fixation.draw()
        win.flip()
        wait(fixation_dur)

        is_dual = condition == 'dual'
        tap_index = 0
        tap_count = 0
        tap_errors = 0
        response = None
        rt = None
        timed_out = False

        stimulus_img.image = trial['img_path']

        kb.clearEvents()
        kb.clock.reset()

        while True:
            stimulus_img.draw()
            prompt.draw()

            if is_dual:
                tap_reminder.draw()
                tap_indicator.text = f"Next key: {tap_keys[tap_index].upper()}"
                tap_indicator.draw()

            win.flip()

            if kb.clock.getTime() >= max_rt:
                timed_out = True
                break

            valid_keys = ['f', 'j', 'escape'] + (tap_keys if is_dual else [])
            pressed = kb.getKeys(keyList=valid_keys, waitRelease=False)

            for k in pressed:
                if k.name == 'escape':
                    win.close()
                    quit()

                if k.name in ('f', 'j') and response is None:
                    response = k.name
                    rt = k.rt

                elif is_dual and k.name in tap_keys:
                    if k.name == tap_keys[tap_index]:
                        tap_count += 1
                        tap_index = (tap_index + 1) % len(tap_keys)
                    else:
                        tap_errors += 1

            if response is not None:
                break

        correct = (not timed_out) and (response == trial['correct_key'])
        if correct:
            block_correct += 1

# check tapping compliance (dual-task trials only)
        if is_dual and rt is not None:
            expected_taps = rt * tap_rate
            tap_compliance = tap_count >= (expected_taps * 0.5)
        else:
            tap_compliance = None

        #FEEDBACK (practice only)
        if give_feedback:
            if timed_out:
                fb_timeout.draw()
            elif correct:
                fb_correct.draw()
            else:
                fb_incorrect.draw()
            win.flip()
            wait(feedback_dur)

        #SAVE TRIAL
        alldata.append({
            'participant_id': exp_info['Participant ID'],
            'age': exp_info['Age'],
            'gender': exp_info['Gender'],
            'handedness': exp_info['Handedness'],
            'block': block_n,
            'trial': trial_n + 1,
            'condition': condition,
            'angle': trial['angle'],
            'trial_type': trial['trial_type'],
            'correct_key': trial['correct_key'],
            'response': response if response else 'timeout',
            'correct': correct,
            'rt': rt,
            'timed_out': timed_out,
            'tap_count': tap_count,
            'tap_errors': tap_errors,
            'tap_compliance': tap_compliance
        })

    #BLOCK SUMMARY
    accuracy = block_correct / len(trials) * 100
    correct_rts = [d['rt'] for d in alldata if d['block'] == block_n and d['correct'] and d['rt'] is not None]
    mean_rt = (sum(correct_rts) / len(correct_rts) * 1000) if correct_rts else 0

    if condition == 'practice':
        msg.text = f"""Practice complete!

Accuracy: {accuracy:.0f}%

The main experiment now begins.
No feedback will be given during the main blocks.

Remember:
  F = SAME object (just rotated)
  J = DIFFERENT object (mirror image)

Press SPACE to continue."""
    else:
        msg.text = f"""Block {block_n} Complete!

Accuracy: {accuracy:.0f}%
Mean RT (correct trials): {mean_rt:.0f} ms

Press SPACE to continue."""

    msg.draw()
    win.flip()
    wait_for_space()

#SAVE DATA
df = pd.DataFrame(alldata)
filename = f"mental_rotation_{exp_info['Participant ID']}.csv"
df.to_csv(filename, index=False)

#END
msg.text = f"""This is the end of the experiment!

Thank you for participating!

Press SPACE to exit."""
msg.draw()
win.flip()
wait_for_space()

win.close()
quit()
