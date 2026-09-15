

import View from "./walkthroughview.js"


export default class WalkThrough{


    constructor(){

        this.init()

    }


    init(){

    
        const path = 'https://ddev.propa360.com/controller/twophotos/walkthrough.json'


        $.getJSON(path,data=>{

            console.log(data)

            this.view = new View(data)


        })



    }





}