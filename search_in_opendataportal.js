// ==UserScript==
// @name         ExampleScript
// @namespace    https://data.europa.eu/
// @version      0.1
// @description  try to take over the world!
// @author       @ralvarezluna
// @match        https://data.europa.eu/data/datasets?locale=es
// @icon         https://www.google.com/s2/favicons?domain=greasyfork.org
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

     const messages = {
        GET_DATA: '🔃 GETTING DATA',
        POST_DATA: '➡️ POST DATA',
        SUCCESS: '🆗 SE HAN ENCONTRADO DATOS ',
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
            let last_modified_date = data[0].metas.modified;
            let last7days = Date.now() - 13;
            if(last_modified_date > last7days)
                alert(messages.SUCCESS + "Existen datasets asociados a su query actualizados en la última semana");
            else{
                alert("No hay actualizaciones recientes relacionadas a su búsqueda");}
          console.log(JSON.parse(request.response));
        } else {
          console.log(`error ${request.status} ${request.statusText}`);
          alert(messages.FAIL);}};
})();