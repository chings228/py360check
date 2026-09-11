
 
 export default class Notification{

    events = {}
    

    constructor(){


    }


    fire(eventName, data){

      const callbacks = this.events[eventName]

      if (callbacks){

        callbacks.forEach(callback=>{
          callback(data)
        })
      }


    }

    

    on(eventName, callback){
      
       if (this.events[eventName]){

          this.events[eventName].push(callback)
       } 
       else{
        this.events[eventName] = [callback];
       }

    }

    off(eventName){

      const event = this.events[eventName]

      if (event){
        delete this.events[eventName];
      }
      

    }


}