var factors = {
    stimulus: ["experiment_4_files/cat1.jpg", "experiment_4_files/cat2.jpg", "experiment_4_files/cat3.jpg"]
    stimulus_duration: [400, 800, 1200]
};

var factorial_values = jsPsych.randomization.factorial(factors);
console.log(JSON.stringify(factorial_values));


jsPsych.init({
    timeline: factorial_values,
});
