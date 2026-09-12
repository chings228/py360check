
export default class Core{



    constructor(){



        this.init()


    }

    init(){

        this.code = Common.getUrlParameter('code')

        console.log(this.code)



        $.getJSON(`fovresult-${this.code}.json`,data=>{


            this.spots = data.spotlist

            console.log(this.spots)

            this.createView()

        })


    }


    createView(){

        this.filepath = `photo_${this.code}`

        let html = ''


        this.spots.forEach(spot => {

            const photolink = `${this.filepath}/${spot}.jpg`


            html += `<div class=photowrap ><div class=name>${spot}</div><img class=photo src=${photolink}></div>`

            
        });



        $("#outer").html(html)






    }


}