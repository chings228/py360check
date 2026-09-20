export default class Common{




    static degToRad(angle){

        return angle * Math.PI / 180
    }

    static radToDeg(angle){

        return angle * 180 / Math.PI
    }


    static dformat(num){

        return (Math.round(num * 100) / 100).toFixed(2);
    }




    static getUrlParameter(sParam) {

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


        static   api(param) {
            var url = '';
            var baseurl = '';
        
        
            baseurl = "https://ddev.propa360.com/controller/twophotos"        
        
            var result;
        
            url = `${baseurl}/${param.method}`;

    
    
            console.log(param)
            return new Promise((resolve, reject) => {
            $.post(url, param, (data) => {
    
    
        
              result = JSON.parse(data);
    
              resolve(result);
            }).fail((error) => {
              console.log(error)
              reject(error);
            });
            });
            }



  
    static   makeid(length) {
      let result = '';
      const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      const charactersLength = characters.length;
      let counter = 0;
      while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        counter += 1;
      }
      return result;
  }


}