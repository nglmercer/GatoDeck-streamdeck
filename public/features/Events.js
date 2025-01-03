import { Giftsparsed, mapselectgift } from '../assets/gifts.js';
import DynamicTable, { EditModal } from '../components/renderfields.js';
import { databases, IndexedDBManager, DBObserver } from '../database/indexdb.js'
import { Counter, flattenObject, TypeofData,ComboTracker, replaceVariables, compareObjects, unflattenObject } from '../utils/utils.js'
import showAlert from '../components/alerts.js';
import { GiftElementsManager } from '../components/renderhtml.js'
import { ActionsManager } from './Actions.js'
import { getTranslation, translations } from '../translations.js';
const ObserverEvents = new DBObserver();
const EventsManager = new IndexedDBManager(databases.eventsDB,ObserverEvents);
async function EventsManagermap(data) {
  const alldata = await ActionsManager.getAllData()
/*console.log("alldatainit",alldata)
  const mapedevents = alldata.map(data => ({
    value: data.id,
    label: data.nombre,
  }))
  console.log("alldata",mapedevents) 
  function async que se invoca a si mismo seria:
  (async () => {
  const mapedevents = await EventsManagermap()
  console.log("mapedevents",mapedevents)
})()*/
  return  alldata.map(data => ({
    value: data.id,
    label: data.nombre,
  }))
}
const newmodalevent = document.getElementById('eventformModal')
const testdata = {
  nombre: getTranslation('nombre_del_evento'),
  eventType: "chat",
  chat: "default text",
  like: 10,
  gift: 5655,
  Actions: [],
  id: undefined,
}

const eventform = document.createElement('dynamic-form');
        eventform.initialize()
            .addField({
                type: 'text',
                name: 'nombre',
                label: 'nombre de evento',
                value: 'nombre de evento',
            })
            .addField({
                type: 'radio',
                name: 'eventType',
                label: 'type',
                options: [
                    { value: 'chat', label: 'chat' },
                    { value: 'gift', label: 'gift' },
                    { value: 'bits', label: 'bits' },
                    { value: 'follow', label: 'follow' },
                    { value: 'subscribe', label: 'subscribe' },
                ],
                value: 'gift',
            })
            .addField({
                type: 'textarea',
                name: 'chat',
                label: 'chat',
                value: 'chat',
                showWhen: {
                    field: 'eventType',
                    value: 'chat'
                }
            })
            .addField({
                type: 'flexible-modal-selector',
                name: 'gift',
                label: 'gift',
                value: 5655,
                options: mapselectgift,
                showWhen: {
                    field: 'eventType',
                    value: 'gift'
                }
            })
            .addField({
                type: 'number',
                name: 'bits',
                label: 'bits',
                value: 'bits',
                showWhen: {
                    field: 'eventType',
                    value: 'bits'
                }
            })
            .addField({
                type: 'number',
                name: 'id',
                label: '',
                hidden: true,
            })
            .addField({
                type: 'flexible-modal-selector',
                name: 'Actions',
                label: 'selecciona la accion',
                mode: 'multi',
                options: await EventsManagermap(),
                value: [],
            })
            .render()
            .toggleDarkMode(true);
eventform.addEventListener('form-submit', async (e) => {
  console.log('Datos modificados:', e.detail);
  const modifiedData = unflattenObject(e.detail);
  console.log("modifiedData",modifiedData, flattenObject(modifiedData))
  const alldata = await EventsManager.getAllData()
  console.log("alldata",alldata)
  
  const keysToCheck = [
    { key: 'eventType', compare: 'isEqual' },
/*       { key: 'gift', compare: 'isEqual' },
*/  { key: modifiedData.eventType, compare: 'isEqual' }
  ];    
  const callbackFunction = (matchingObject, index, results) => {
    console.log(`Objeto coincidente encontrado en el índice ${index}:`, matchingObject, results);
  };
  
  const results = compareObjects(modifiedData, alldata, keysToCheck, callbackFunction);
  console.log("results",results)
  if (!results.validResults.length >= 1 && !modifiedData.id) {
    newmodalevent.close();
    EventsManager.saveData(modifiedData)
    showAlert('success','Se ha guardado el evento')
  } else if (modifiedData.id && results.validResults.length <= 1) {
    newmodalevent.close();
    EventsManager.updateData(modifiedData)
    showAlert('success','Se ha guardado el evento')
  } else {
    console.log(modifiedData.id,"id de la base de datos")
    showAlert('error','ya existe un elemento en la base de datos igual')
  }
});
eventform.addEventListener('form-change', (e) => {
  console.log('Form values changed:', e.detail);
});
newmodalevent.appendChild(eventform);
/* setTimeout(() => {
  eventform.reRender(testdata);
}, 1000);
newmodalevent.open(); */


/* const EventsModal = document.getElementById('EventsModal');
 */

/* const Formelement = new EditModal(await getEventconfig(), testdata);
const Eventsformelement = Formelement.ReturnHtml(testdata);  */


/*tabla de Eventos para modificar y renderizar todos los datos*/
const callbacktable = async (data,modifiedData) => {
/*   const datamodal = unflattenObject(modifiedData);
  console.log("callbacktable",data,datamodal); */
  eventform.reRender(modifiedData);
  newmodalevent.open();
}
const callbacktabledelete = async (data,modifiedData) => {
  console.log("callbacktabledelete",data,modifiedData);
  const index = await table.getRowIndex(data);
  table.removeRow(index);
  EventsManager.deleteData(data.id)
}
const configtable = {
    nombre: {
      class: 'input-default',
      type: 'text',
      returnType: 'string',
    },     
    eventType: {
      class: 'radio-default',
      type: 'radio',
      toggleoptions: true,
      returnType: 'string',
      options: [{ value: 'chat', label: 'Chat' }, { value: 'follow', label: 'Seguimiento' },{ value: 'like', label: 'like'},
      {value: 'share', label: 'compartir'}, { value: 'subscribe', label: 'suscripcion' }, { value: 'gift', label: 'Gift' }],
    },
    buttonsave: {
      class: 'default-button',
      type: 'button',
      label: getTranslation('edit'),
      callback: callbacktable,
    },
    buttondelete: {
      class: 'default-button deletebutton',
      type: 'button',
      label: getTranslation('delete'),
      callback: callbacktabledelete,
    },
}

const table = new DynamicTable("#table-containerEvent",configtable);
(async () => {
  const alldata = await EventsManager.getAllData()
  alldata.forEach((data) => {
    table.addRow(data);
  });
  console.log("alldata render table",alldata);
})  (); 
ObserverEvents.subscribe(async (action, data) => {
  if (action === "save") {
    table.clearRows();
    const dataupdate = await EventsManager.getAllData();
    dataupdate.forEach((data) => {
      table.addRow(data);
    });
  } else if (action === "delete") {
/*     table.clearRows();
    const dataupdate = await EventsManager.getAllData();
    dataupdate.forEach((data) => {
      table.addRow(data);
    }); */
  }
  else if (action === "update") {
    table.clearRows();
    const dataupdate = await EventsManager.getAllData();
    dataupdate.forEach((data) => {
      table.addRow(data);
    });
    showAlert ('info', "Actualizado", "1000");
  }
});

const giftlistmanager = new GiftElementsManager(mapselectgift);

const handleProductClick = (product) => {
    console.log('Producto seleccionado:', product);
};

/* giftlistmanager.renderToElement('giftmap', handleProductClick);
 */

export { EventsManager }