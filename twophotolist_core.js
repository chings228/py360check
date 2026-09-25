
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



             const path = 'https://ddev.propa360.com/controller/twophotos/walkthrough.json'

             console.log(path)
            
             $.get(path , str=>{

                console.log("sdfsdf")

                console.log("str",str)

                if (str.trim() != ''){
                    this.createView(JSON.parse(str))
                }
                else{

                    let data = {}
                    data.link = {}

                    this.createView(data)
                }

            

            },"text")




   

        })


    }





    createView(data){


        const link = data.link
        console.log("link",link)


        this.filepath = `photo_${this.code}`

        let html = ''


        this.spots.forEach(spot => {

            const photolink = `${this.filepath}/${spot}.jpg`


            let linktext = ``

            console.log(spot)

            if (link[spot]){

                console.log("link exist")

                for (const neighbour in link[spot]){

                    console.log("neighbour",neighbour)

                    const info = link[spot][neighbour]

                    const linkstr = `./two_photos.html?code=${this.code}&sourcespot=${spot}&sourcepitch=${info.sourcepitch}&sourceyaw=${info.sourceyaw}&targetspot=${info.targetspot}&targetpitch=${info.targetpitch}&targetyaw=${info.targetyaw}`

                    console.log(linkstr)

                    linktext += `<a target=_new href=${linkstr}>${info.targetspot} s ${info.sourceyaw} t ${info.targetyaw}</a><br>`

                }



            }








            html += `<div class=photowrap id=${spot} >
            <div class=name>${spot}</div>
            <img class=photo src=${photolink}>
            <div class =link>${linktext}</div>
            </div>`

            
        });



        $("#outer").html(html)










    }


}