var hello_trial = {
    type: 'html-keyboard-response',
    stimulus: 'Hello world!'
}

var image_trial = {
    type: 'image-keyboard-response',
    stimulus: "experiment_1_files/person.jpg"
}

var trials = [hello_trial, image_trial]

var repeated_trials = jsPsych.randomization.repeat(trials,5);

jsPsych.init({
    timeline: repeated_trials,
    on_finish: function() {
        jsPsych.data.displayData();
    }
});
