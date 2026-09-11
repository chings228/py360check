
import View from "./twophotos_view.js";


export default class Core{



    constructor(){



        this.init()

    }


    getUrlParameter(sParam) {

        console.log("geturl",sParam)
          var sPageURL = window.location.search.substring(1);
          var sURLVariables = sPageURL.split('&');
    
          for (var i = 0; i < sURLVariables.length; i++) {
            var sParameterName = sURLVariables[i].split('=');
    
            var key = sParameterName[0];
    
            if (key == sParam) {
              return sParameterName[1];
            }
          }
        }



    init(){

        this.code = this.getUrlParameter('code')

        console.log(this.code)



        $.getJSON(`fovresult-${this.code}.json`,data=>{


            this.spots = data.spotlist

            console.log(this.spots)

            this.createView()

        })






    }


    createView(){

        const data = {}
        data.spots = this.spots
        data.type = "source"
        data.code = this.code

        this.sourceView  = new View(data)

        data.type = "target"

        this.targetView = new View(data)




    }




}