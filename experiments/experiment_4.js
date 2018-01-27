var factors = {
    stimulus: ["experiment_4_files/cat1.jpg", "experiment_4_files/cat2.jpg", "experiment_4_files/cat3.jpg"],
    stimulus_duration: [400, 800, 1200]
};

var factorial_values = jsPsych.randomization.factorial(factors);
console.log(JSON.stringify(factorial_values));

var trial = {
    type: 'image-keyboard-response',
    prompt: '<p>Press a key!</p>',
    stimulus: jsPsych.timelineVariable('stimulus'),
    stimulus_duration: jsPsych.timelineVariable('stimulus_duration')
};

var trials_with_variables = {
    timeline: [trial],
    timeline_variables: factorial_values
};

jsPsych.init({
    timeline: [trials_with_variables],
    on_finish: function() {
        jsPsych.data.displayData();
    }
});
