// ==UserScript==
// @name         ExampleScript
// @namespace    scripts.ua.es
// @version      0.1
// @description  try to take over the world!
// @author       @ralvarezluna
// @match        https://datosabiertos.dipcas.es/pages/frontpage/
// @icon         https://www.google.com/s2/favicons?domain=greasyfork.org
// @grant        none
// ==/UserScript==

(function() {
  'use strict';

   const messages = {
      GET_DATA: '🔃 GETTING DATA',
      POST_DATA: '➡️ POST DATA',
      SUCCESS: '🆗 Su búsqueda ha arrojado resultados ',
      FAIL: '😡 FAIL',
    };
    const notificationSounds = {
      'SUCCESS': 'https://notificationsounds.com/storage/sounds/file-sounds-942-what-friends-are-for.ogg',
      'FAIL': 'https://notificationsounds.com/storage/sounds/file-sounds-1126-accomplished.ogg'
    };
    let query = prompt('Query', '');
    let request = new XMLHttpRequest();
    request.open("GET", "https://datosabiertos.dipcas.es/api/datasets/1.0/search/?q=" + query);
    request.send();
    request.onload = () => {
      console.log(request);
      if (request.status === 200) {
        // by default the response comes in the string format, we need to parse the data into JSON
          const jsonObj = JSON.parse(request.response);
          const data = jsonObj['datasets'];
          if(data.length > 0)
          {
            console.log(data);
            //const result = Object.assign(...data.map(({datasetid, fields}) => ({[datasetid]: fields})))
            let res=[];
            data.forEach(element => {
               res += element.datasetid + '\n';
            });
            alert(messages.SUCCESS + '\n' + "Los datos asociados a su query en dataset(s): " + res);
          }
          else{
              alert("No hay datos relacionados a su búsqueda");}
        console.log(JSON.parse(request.response));
      } else {
        console.log(`error ${request.status} ${request.statusText}`);
        alert(messages.FAIL);}};
})();