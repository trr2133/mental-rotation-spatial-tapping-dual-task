# Mental Rotation with Spatial Tapping Dual-Task Experiment

This repository contains a PsychoPy experiment examining whether a concurrent spatial tapping task, which selectively loads the visuospatial sketchpad, disrupts mental rotation performance, and whether any interference interacts with the angular disparity of the stimuli.

---

## Background

### Mental Rotation

Mental rotation is the cognitive process by which we mentally transform spatial representations of objects. Shepard and Metzler (1971) introduced the canonical paradigm: participants judge whether two three-dimensional objects are the same shape or mirror images. Their key finding was that reaction time increases linearly with the angular difference between the objects, and is one of the most replicated results in cognitive psychology, suggesting that mental rotation is an analogue process, not a symbolic one.

### The Visuospatial Sketchpad

Baddeley and Hitch's (1974) working memory model proposes a multicomponent system for temporarily storing and manipulating information. It consists of the phonological loop, which handles verbal material, the visuospatial sketchpad (VSSP), which stores visual and spatial information, and the central executive, which coordinates and controls both. Logie (1995) further proposed that the VSSP itself consists of two subcomponents: the visual cache, which passively stores visual form information such as colour and shape, and the inner scribe, which handles spatial and movement information and is responsible for rehearsing and manipulating spatial representations. Mental rotation requires actively transforming a spatial representation, making the inner scribe the theoretically relevant component. Spatial tapping (i.e., repeating a fixed sequence of spatial keypresses) has been validated as a method that selectively loads the inner scribe without engaging verbal resources (Farmer, Berman, & Fletcher, 1986), making it an ideal secondary task for testing whether spatial working memory specifically underlies mental rotation.

### Research Question

Does loading the visuospatial sketchpad via concurrent spatial tapping impair mental rotation performance? 

Ebert et al. (2025) found that a visual working memory load did not specifically disrupt the rotation process, but their secondary task targeted the visual cache rather than the spatial component. The present experiment addresses this directly by using spatial tapping as the secondary task, providing a more precise test of whether spatial working memory specifically underlies mental rotation.

Specifically:

1. Is accuracy lower and reaction time slower in the dual-task (rotation + tapping) condition compared to the single-task (rotation only) condition?
2. Does the tapping interference interact with angular disparity — is it greater at larger rotation angles, where the rotation process is more demanding?

---

## Experimental Design

**Design:** Within-subjects, 2 x 4 factorial

| Factor | Levels |
|--------|--------|
| Condition | Single-task (rotation only) vs. Dual-task (rotation + tapping) |
| Angle | 0, 50, 100, 150 degrees (Ganis & Kievit, 2015) |

**Trial structure:**
1. Fixation cross (500 ms)
2. Stimulus display — two 3D Shepard-Metzler objects shown side by side
3. Participant responds: F = same object (rotated), J = different (mirror image)
4. In dual-task blocks, participant simultaneously taps a 4-key sequence with their non-dominant hand throughout the trial

**Block structure:**
- 8 practice trials (single-task only, with feedback)
- Block 1 and Block 2: single-task and dual-task (order counterbalanced across participants)
- 20 trials per angle per condition = 80 trials per block = 160 experimental trials total

**Tapping sequence:**
- Right-handed participants: Z -> X -> C -> V (left to right, left/non-dominant hand)
- Left-handed participants: / -> . -> , -> M (right to left, right/non-dominant hand)

Tapping keys are assigned automatically based on handedness entered in the dialog box. This ensures the non-dominant hand is always used for tapping, making the task equally fair for left- and right-handed participants. The key positions are mirror images on the keyboard, ensuring equivalent difficulty for both groups.

**Dependent variables:**
- Reaction time (RT) on correct trials
- Accuracy (proportion correct)
- Tapping count, tapping errors, and tapping compliance (dual-task block only)

---

## Stimuli

This experiment uses the Ganis and Kievit (2015) stimulus set, used under open access terms (CC BY 4.0). Full citation in the references section below.

The stimulus set consists of 48 three-dimensional Shepard-Metzler objects rendered with shading and depth cues, validated at four angular disparities: 0, 50, 100, and 150 degrees. Each image contains both shapes side by side on a black background. Half of all pairs show the same object at different rotations, and half show mirror images. 

**To set up the stimuli:**

1. Download the stimuli from: https://figshare.com/articles/dataset/A_new_set_of_three_dimensional_stimuli_for_investigating_mental_rotation_processes/1045385
2. Download the file called `all stimuli as jpg.zip`
3. Extract the zip and rename the extracted folder to `stimuli`
4. Place the `stimuli` folder in the same directory as the experiment script

The folder structure should look like this:

```
mental-rotation-spatial-tapping-psychopy/
├── mental_rotation_experiment.py
├── trials.csv
├── README.md
└── stimuli/
    ├── 1_0.jpg
    ├── 1_0_R.jpg
    ├── 1_50.jpg
    └── ...
```

Files without `_R` in the name are same-object pairs. Files with `_R` are mirror-image (different) pairs. The number before the first underscore is the object ID, and the number after is the rotation angle in degrees.

---

## How to Run

Install PsychoPy from https://www.psychopy.org/download.html

Open `mental_rotation_experiment.py` in the PsychoPy Coder and click Run. A dialog box will appear asking for Participant ID, Age, Gender, and Handedness. The experiment will then run automatically.

**Response keys:**

| Key | Action |
|-----|--------|
| F | Same (objects are the same, just rotated) |
| J | Different (objects are mirror images) |
| Z X C V | Tapping sequence for right-handers (left hand) |
| M , . / | Tapping sequence for left-handers (right hand) |
| Escape | Quit experiment |

---

## Parameters

All parameters can be adjusted at the top of `mental_rotation_experiment.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `angles` | [0, 50, 100, 150] | Rotation angles in degrees (Ganis & Kievit, 2015) |
| `n_practice` | 8 | Number of practice trials |
| `n_trials_per_angle` | 20 | Trials per angle per condition |
| `fixation_dur` | 0.5 | Fixation cross duration (seconds) |
| `max_rt` | 10.0 | Maximum response time (seconds) |
| `feedback_dur` | 0.5 | Feedback display duration (seconds) |

---

## Output

Data is saved to `mental_rotation_{Participant ID}.csv` in the same folder as the script.

| Column | Description |
|--------|-------------|
| `participant_id` | Participant ID |
| `age` | Participant age |
| `gender` | Participant gender |
| `handedness` | Participant handedness |
| `block` | Block number (0 = practice) |
| `trial` | Trial number within block |
| `condition` | practice, single, or dual |
| `angle` | Rotation angle (0, 50, 100, 150) |
| `trial_type` | same or different |
| `correct_key` | Expected response key |
| `response` | Participant response or timeout |
| `correct` | True or False |
| `rt` | Reaction time in seconds |
| `timed_out` | True if no response within 10 seconds |
| `tap_count` | Correct taps in sequence (dual-task only) |
| `tap_errors` | Out-of-sequence keypresses (dual-task only) |
| `tap_compliance` | True if tap count >= 50% of expected taps |

---

## Expected Results

Based on Shepard and Metzler (1971), we expect:

- **Angle effect:** RT should increase linearly with rotation angle in both conditions, replicating the classic mental rotation effect
- **Condition effect:** If the VSSP contributes to mental rotation, RT should be slower and/or accuracy lower in the dual-task condition
- **Interaction:** If spatial load specifically disrupts the rotation process, the condition effect should be larger at greater angles

A null interaction would suggest that mental rotation does not draw specifically on spatial working memory resources, consistent with Ebert et al. (2025).

---

## Analysis

Data can be analysed by filtering out practice trials and excluding dual-task trials where tap_compliance is false. Mean reaction time (correct trials only) and accuracy can then be summarised by condition and angle.
A 2 (condition) x 4 (angle) repeated-measures ANOVA is recommended for both RT and accuracy, with the following planned comparisons:

A main effect of condition (single vs. dual) to test whether spatial tapping impairs performance
A main effect of angle to confirm the classic linear rotation effect via planned linear contrast
A condition x angle interaction to test whether tapping interference is greater at larger rotation angles

If the interaction is significant, post-hoc pairwise comparisons between conditions at each angle level are recommended to identify where the effect emerges.

---

## References

- Baddeley, A. D., & Hitch, G. (1974). Working memory. *Psychology of Learning and Motivation*, 8, 47-89.
- Ebert, W. M., Jost, L., Jansen, P., Stevanovski, B., & Voyer, D. (2025). Visual working memory as the substrate for mental rotation: A replication. Psychonomic Bulletin & Review, 32(3), 1204-1216.
- Farmer, E. W., Berman, J. V., & Fletcher, Y. L. (1986). Evidence for a visuo-spatial scratch-pad in working memory. The Quarterly Journal of Experimental Psychology Section A, 38(4), 675-688.
- Ganis, G., & Kievit, R. A. (2015). A new set of three-dimensional shapes for investigating mental rotation processes: validation data and stimulus set. Journal of Open Psychology Data, 3(1), e3-e3.
- Logie, R. H. (2014). Visuo-spatial working memory. Psychology Press.
- Shepard, R. N., & Metzler, J. (1971). Mental rotation of three-dimensional objects. Science, 171(3972), 701-703.
