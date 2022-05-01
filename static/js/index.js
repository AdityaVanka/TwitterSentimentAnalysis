// const urls = [pieChartDataUrl, barChartDataUrl, lineChartDataUrl, bubbleChartDataUrl, wordCloudDataUrl];

const urls = [wordCloudDataUrl];
var myBar = [{gender: "Male", cnt: "100"},{gender: "Female", cnt: "90" }];
//var myBar = [{'gender': 'Male', 'cnt': '100'}, {'gender': 'Female', 'cnt': '90'}];
var myWords = [{word: "Running", size: "10"}, {word: "Surfing", size: "20"}, {word: "Climbing", size: "50"}, {word: "Kiting", size: "30"}, {word: "Sailing", size: "20"}, {word: "Snowboarding", size: "60"} ];

Promise.all(urls.map(url => fetch(url).then(res => res.json()))).then(run);

function run(dataset) {
    // console.log(dataset[0]);
    // draw_barChart(dataset[0]);
    wordCloud(dataset[0]);
};