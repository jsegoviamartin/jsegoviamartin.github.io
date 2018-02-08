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
    on_finish: function(){
        var experiment_data = jsPsych.data.get();
        saveData("test.csv", experiment_data.csv());
    }
});

function saveData(name, data){
    var url = 'record_result.php';
    var data = {filename: name, filedata: data};
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: new Headers({
                'Content-Type': 'application/json'
        })
    });
}
