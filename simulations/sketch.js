
var s1,s2,s3,s4,s5,s6;
let myFont;


function preload(){
    s1 = new Sim("institution 1",16, 30,30,"https://raw.githubusercontent.com/AshaSato/PhD-Snippets/master/inst1_16.csv");
    s2 = new Sim("institution 2",16, 440,30,"https://raw.githubusercontent.com/AshaSato/PhD-Snippets/master/inst2_16.csv");
    s3 = new Sim("institution 2",16, 840,30,"https://raw.githubusercontent.com/AshaSato/PhD-Snippets/master/inst3_16.csv");
    s4 = new Sim("low inequality",16, 30,380,"https://raw.githubusercontent.com/AshaSato/PhD-Snippets/master/inst_low_ineq.csv");
    s5 = new Sim("mid inequality",16,440,380,"https://raw.githubusercontent.com/AshaSato/PhD-Snippets/master/inst_mid_ineq.csv");
    s6 = new Sim("high inequality",16,840,380,"https://raw.githubusercontent.com/AshaSato/PhD-Snippets/master/inst_high_ineq.csv");
}

function setup() {
  // put setup code here
  createCanvas(1920,1080);
  noStroke();
  textSize(18);

  s1.parseDataTable();
  s2.parseDataTable();
  s3.parseDataTable();
  s4.parseDataTable();
  s5.parseDataTable();
  s6.parseDataTable();


  print("targetgrid");
  print(s2.targetGrid);

  print("currentgrid:");
  print(s1.currentGrid);
  frameRate(2);
}

function draw() {

    background(255);

  s1.displaySimulation();
  s2.displaySimulation();
  s3.displaySimulation();
  s4.displaySimulation();
  s5.displaySimulation();
  s6.displaySimulation();

}


//this code assumes microcommunities 8x8 - animates 1 microcommunity object
class Sim {
    constructor(label, size, xpos,ypos, fileloc) {
        this.label = label;

        this.size = size;

        this.x = xpos;
        this.y = ypos;

        this.datatable = loadTable(fileloc, "csv", "header");

        this.generation = 0;

        this.signalColours = [color("#990000"),color("#ff0000"),color("#ff9900"),color("#ffcc00"),
                            color("#99cc00"),color("#493C2B"),color("#A46422"),color("#EB8931"),
                            color("EB8931"),color("#00cc99"),color("#009999"),color("#0099ff"),
                            color("#0000ff"),color("#6600ff"),color("#9900cc"),color("#cc0099"),


                            color(255)]

        this.emptyGrid = make2Darray(this.size,this.size); //initialise empty grid
        this.targetGrid= make2Darray(this.size,this.size);; //parsed datafile with final signal Colours in each cell
        this.currentGrid = make2Darray(this.size,this.size); //

    }

    parseDataTable() {
        for(var i = 0; i < this.size; i++){
            for(var j = 0; j < this.size; j ++){
                this.targetGrid[i][j] = this.datatable.getNum(i,j);
            }
        }

        for(var i = 0; i < this.size; i++){
            for(var j = 0; j < this.size; j ++){
                this.currentGrid[i][j] = 17; //white
            }
        }
    }


    drawGrid() {
        //draw title
        fill(0);
        text(this.label, this.x,this.y-10);
        //draw empty grid
        for (var i = 0; i < this.size; i++) {
            for(var j = 0; j < this.size; j ++) {
                //iterate over rows

                var xoff= this.x; //set position
                var yoff = this.y;

                var x = xoff +i *20; //offset
                var y = yoff + j *20;

                var c = this.signalColours[(this.currentGrid[j][i])-1];
                //print(c);
                fill(c);
                //fill(255);
                rect(x,y,20,20);
            }
        }
    }

    increaseGeneration(){

        if(this.generation == this.size) { //loop
            this.generation = 0;
            for(var i = 0; i < this.size; i++){
                for(var j = 0; j < this.size; j ++){
                    this.currentGrid[i][j] = 17; // white
                }
            }
        } else {

            for(var i = 0; i < this.size; i ++) {
                this.currentGrid[this.generation][i] = this.targetGrid[this.generation][i];
                //print(this.currentGrid);
            }

            this.generation +=1;
        }

    }


    displaySimulation(){
        this.drawGrid();
        this.increaseGeneration();

    }

}

function make2Darray(cols,rows) {
    var arr = new Array(cols);
    for (var i = 0; i < arr.length; i++) {
        arr[i] = new Array(rows);
    }
    return arr;
}

function keyPressed() {
    print("key pressed");
    if (keyCode === RIGHT_ARROW) {
        s1.increaseGeneration();
    }

}
