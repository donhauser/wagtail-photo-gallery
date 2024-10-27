
let lazySasModule = import("./select-and-sort.js")

let formsetReadyPromise = new Promise(resolve => {
    document.addEventListener('w-formset:ready', (event) => resolve(event), {once: true});
})

async function* formsetAddedPromiseGenerator(panel) {
    
    while(true) {
        let promise = new Promise(resolve => {
            document.addEventListener('w-formset:added', (event) => resolve(event), {once: true});
        });
        
        panel.addForm();
        
        yield await promise;
    }
}

/**
 * This handler manages the interaction with the InlinePanel
 * 
 * As of oct 2024, it was not possible to simply inherit from InlinePanel.
 * Thus, the interaction is provided by the two events 'w-formset:ready' and 'w-formset:added',
 * which are wrapped with async/await
 */
class AlbumImagePanelHandler {
    constructor(panel, options) {
        this.panel = panel
        
        this.coverField = $(options.coverField)
        
        this.addButton = $(options.addButton)
        this.selectButton = $(options.selectButton)
        this.unselectButton = $(options.unselectButton)
        this.deleteButton = $(options.deleteButton)
        
        this.formsetAdded = formsetAddedPromiseGenerator(this.panel);
    }
    
    async initialize() {
        let module = await lazySasModule;
        let event = await formsetReadyPromise;
        
        this.sas = new module.SelectAndSort(
            event.target,
            {
                sortUpdate: instance => {
                    // update all orders according to new sorting
                    instance.element.children().each((index, e) => {
                        $('input[name$="-ORDER"]', e).val(index+1)
                    })
                },
                selectChange: (instance, element) => {
                    this.selectButton.prop("disabled", instance.checkAllSelected())
                },
                selectModeChange: (instance, value) => {
                    this.addButton.prop("disabled", value)
                    this.selectButton.prop("disabled", instance.checkAllSelected())
                    this.unselectButton.prop("disabled", !value)
                    this.deleteButton.prop("disabled", !value)
                },
                delete: (instance, elem) => {
                    $('input[name$="-DELETE"]', elem).val(1);   
                },
                coverChange: (element) =>  {
                    if(element) {
                        // lookup the django id of the clicked element and put it in the <input> field
                        let new_cover = $('input[name$="-id"]', element).val();
                        this.coverField.val(new_cover);
                    } else { // element = undefined unsets the cover
                        this.coverField.val();
                    }
                }
            }
        );
        
        this.initializeCover(event.target);
        this.initializeDragAndDrop(event.target);
        
        this.addButton.click(() => this.showImageFileChooser())
        this.selectButton.click(() => this.sas.selectAll())
        this.unselectButton.click(() => this.sas.unselectAll())
        this.deleteButton.click(() => this.sas.deleteSelected())
    }
    
    initializeCover(target) {
        // find the input containing the cover id and add the .cover-image class to the correct <li>
        let value = this.coverField.val();
        let inputField = $(target).find('input[name$="-id"][value="'+value+'"]')
        
        inputField.parents(".ui-sortable-handle").addClass("cover-image")
    }
    
    initializeDragAndDrop(target) {
        target.ondrop = (e) => {$(target).removeClass("drag-highlight drag-highlight-hover"); this.dropHandler(e)}
        target.ondragover = (e) => {e.preventDefault(); $(target).addClass("drag-highlight-hover")};
        target.ondragleave = (e) => $(target).removeClass("drag-highlight-hover");
        
        $(window).on('dragover', (e) => {$(target).addClass("drag-highlight")});
        $(window).on('dragleave', (e) => {$(target).removeClass("drag-highlight")});
    }
    
    async addImages(files) {
        // iterate over the user selected upload files
        for (const file of files) {
            
            let reader = new FileReader();
            reader.readAsDataURL(file);
            
            let imageTag = await new Promise(resolve => reader.onload = (readerEvent) => {
                let image = new Image();
                image.src = readerEvent.target.result;
                image.onload = () => resolve(image);
            });
            
            // wait until the formset child was added by the InlinePanel
            let formsetAddedEvent = (await this.formsetAdded.next()).value
            let target = formsetAddedEvent.target;
            
            let dataTransfer = new DataTransfer();
            let imageInput = $(`#${formsetAddedEvent.detail.formsetPrefix}-${formsetAddedEvent.detail.formIndex}-image`).get(0)
            
            dataTransfer.items.add(file);
            imageInput.files = dataTransfer.files
            
            $(target).find('label').replaceWith(imageTag)
            
            this.sas.addElement(target);
        }
    }
    
    showImageFileChooser() {
        let fileInput = $('<input type="file" multiple="multiple"/>');
        
        fileInput.get(0).addEventListener('change', (inputEvent) => this.addImages(inputEvent.target.files));
        
        fileInput.click();
        
    }
    
    dropHandler(ev) {
        // Prevent file from being opened
        ev.preventDefault();
        
        this.addImages(ev.dataTransfer.files)
    }
}
