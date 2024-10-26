
var lazyModule = import("./select-and-sort.js")

document.addEventListener('w-formset:ready', async (event) => {
    let module = await lazyModule;
    
    let coverField = $("#id_cover")
    let prefix = event.detail.formsetPrefix
    
    let buttonAdd = $(`#${prefix}-ADD`)
    let buttonSelect = $(`#${prefix}-SELECT`)
    let buttonUnselect = $(`#${prefix}-UNSELECT`)
    let buttonDelete = $(`#${prefix}-DELETE`)
    
    var sas = new module.SelectAndSort(
        event.target,
        {
            sortUpdate: instance => {
                
                // update all orders according to new sorting
                instance.element.children().each((index, e) => {
                    $('input[name$="-ORDER"]', e).val(index+1)
                })
            },
            selectChange: (instance, element) => {
                buttonSelect.prop("disabled",instance.checkAllSelected())
            },
            selectModeChange: (instance, value) => {
                buttonAdd.prop("disabled",value)
                buttonSelect.prop("disabled",instance.checkAllSelected())
                buttonUnselect.prop("disabled",!value)
                buttonDelete.prop("disabled",!value)
            },
            delete: (instance, elem) => {
                $('input[name$="-DELETE"]', elem).val(1);   
            },
            coverChange: (element) =>  {
                if(element) {
                    // lookup the django id of the clicked element and put it in the <input> field
                    let new_cover = $('input[name$="-id"]', element).val();
                    coverField.val(new_cover);
                } else { // element = undefined unsets the cover
                    coverField.val();
                }
            }
        }
    );
    
    buttonAdd.click(() => {
        
        let lastChild = $(sas.element).children().last();
        let inputLabel = lastChild.find("label");
        
        sas.addElement(lastChild);
        
        lastChild.find("input").get(0).addEventListener('change', (e) => {

            // getting a hold of the file reference
            let file = e.target.files[0]; 

            // read the user file 
            let reader = new FileReader();
            reader.readAsDataURL(file);
            
            
            reader.onload = readerEvent => {
                // create an image object from the upload file
                let image = new Image();
                
                image.src = readerEvent.target.result;
                
                inputLabel.replaceWith(image)
            }

        })

        // clicking on the label opens the file dialog
        inputLabel.click();
    })
    buttonSelect.click(() => sas.selectAll())
    buttonUnselect.click(() => sas.unselectAll())
    buttonDelete.click(() => sas.deleteSelected())
    
    // find the input containing the cover id and add the .cover-image class to the correct <li>
    let value = coverField.val();
    let idField = $('input[name$="-id"][value="'+value+'"]')
    
    idField.parents(".ui-sortable-handle").addClass("cover-image")
});
