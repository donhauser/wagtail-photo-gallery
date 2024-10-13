



class SelectAndSort {
    /*
     * jQuery UI select and sort widget (for images)
     *
     * Usage:
     *   SelectAndSort(<DOM-element>, options)
     * 
     * Options:
     *   contextMenu(callable):
     *     Extend the context menu.
     *     An array consisting of objects with {class: "css-class", text: "menu entry", click: some_function} is expected.
     *   sortUpdate(callable):
     *     This callback will be triggered when the sorting changes.
     *    
     *  Copyright:
     *   Jonas Donhauser - 2021
     */

    constructor(element, options) {
        if(!options) options = {};
        
        // register target element
        this.element = $(element);
        this.element.addClass("select-and-sort");
        
        // state variables
        this.multiSortMode = false;
        this.selectMode = false;
        this.mousedown_timeout;
        this.selected = false;
        this.rightClickElement;
        
        // append custom contextmenu to <body>
        this.menu = $('<nav>', {id: 'contextMenu', 'class': "select-and-sort"})
        .appendTo($("body"));
        
        
        this.createSortable();
        
        // register callbacks
        if(options["contextMenu"]) {
            this.createContextMenu = options["contextMenu"];
        } else {
            this.createContextMenu = () => [];
        }
        
        if(options["sortUpdate"]) {
            this.sortUpdate = options["sortUpdate"];
        } else {
            this.sortUpdate = () => [];
        }
        
        if(options["selectChange"]) {
            this.selectChangeCallback = options["selectChange"];
        } else {
            this.selectChangeCallback = () => [];
        }
        
        if(options["selectModeChange"]) {
            this.selectModeChangeCallback = options["selectModeChange"];
        } else {
            this.selectModeChangeCallback = () => [];
        }
        
        if(options["delete"]) {
            this.deleteCallback = options["delete"];
        } else {
            this.deleteCallback = () => [];
        }
        
        this.setSelectMode(false);
        
        
        // no context menu on custom context menu
        this.menu.contextmenu(e => e.preventDefault())
        .hide();
        
        // Interaction with mousedown etc.
        this.createEventListeners();
        
    }
    
    createSortable() {
        // create the jQuery UI sortable widget
        
        let self = this;
        
        this.element.sortable({
            placeholder: "ui-state-highlight",
            forcePlaceholderSize: true,
            update: ( event, ui ) => self.sortUpdate(self, event, ui),
            start: () => clearTimeout(self.mousedown_timeout),
            tolerance: "pointer",
            cursor: "move",
            stop: function (event, ui) {
                if(self.multiSortMode) {
                    
                    // move selected element to their new position
                    var selected_children = ui.item.parent().children('.selected');
                    ui.item.after(selected_children);
                    
                    // trigger sort update listeners
                    self.sortUpdate(self, event, ui);
                    
                    if(self.multiSortMode) {
                        self.setMultiSortable(false);
                    }
                }
            }
        })
    }
    
    setMultiSortable(value) {
        // toggle multiple items sortable mode
        
        this.multiSortMode = value;
        
        let element = this.element
        
        if(value) {
            element.sortable("option", "helper", SelectAndSort.multiSortableHelper);
            element.sortable("enable");
        } else {
            element.sortable("option", "helper", "original");
            
            if(this.selectMode) element.sortable("disable");
        }
    }
    
    static multiSortableHelper(e, item) {
        var elements = item.parent().children('.selected').clone();
        
        var helper = $('<li/>');
        return helper.append(elements);
    };


    static createUl(list) {
        return $('<ul>').append(
            list.map(entry => $("<li>", entry))
        )
    }
    
    triggerMultiSort() {
        // trigger the multiple item sorting mode (via fake click event)
        
        this.setMultiSortable(true);
        
        var offset = $(this.element.children(".selected")[0]).offset();
        var event = jQuery.Event('mousedown', {
            which: 1,
            pageX: offset.left,
            pageY: offset.top,
        });
        
        $(this.element.children(".selected")[0]).trigger(event);
    }
    
    
    updateContextMenu(e) {
        // update the context menu (for different menus for different modes)
        let contextMenu;

        let coverText;

        if(!e.hasClass("cover-image")) {
            coverText = "Set as cover";
        } else {
            coverText = "Unset as cover";
        }
        
        if(this.selectMode) {
            contextMenu = [
                {class: "check", text: "Unselect All", click: () => this.unselectAll()},
                {class: "delete", text: "Delete Selected", click: () => this.deleteSelected()},
                {class: "move", text: "Move", click: () => this.triggerMultiSort()},
                
                ...this.createContextMenu(this) // user defined menu
            ];
            
            if(!this.checkAllSelected()) {
                contextMenu.splice(0, 0, {class: "check", text: "Select All", click: () => this.selectAll()});
            }
            
        } else {
            contextMenu = [
                {class: "check", text: "Select All", click: () => this.selectAll()},
                {class: "delete", text: "Delete", click: () => this.deleteElement(this.rightClickElement)},
                {class: "cover", text: coverText, click: () => {
                    if(this.rightClickElement.hasClass("cover-image")) {
                        this.rightClickElement.removeClass("cover-image");
                        $("#id_cover").val();
                    } else {
                        // lookup the django id of the clicked element and put it in the <input> field
                        let new_cover = $('input[name$="-id"]', this.rightClickElement).val();
                        $("#id_cover").val(new_cover);

                        // update css classes
                        $(".cover-image").removeClass("cover-image");
                        this.rightClickElement.addClass("cover-image");
                    }
                }},
                ...this.createContextMenu(this) // user defined menu
            ];
        }
        
        this.menu.html(SelectAndSort.createUl(contextMenu));
    }
    
    setSelectMode(value) {
        // toggle the select mode
        
        this.selectMode = value;
        
        let element = this.element;
        
        element.toggleClass("selectable", value)
        
        //this.updateContextMenu()
        
        if(value) {
            element.sortable("disable");
        }
        else {
            element.sortable("enable");
        }
        
        this.selectModeChangeCallback(this, value)
    }
    
    
    selectAll() {
        // select all images
        
        this.element.children().addClass("selected");
        
        this.setSelectMode(true);
    }
    
    unselectAll() {
        // unselect all images
        
        this.element.children().removeClass("selected");
        
        // automatically exit selectMode
        this.setSelectMode(false);
    }
    
    checkAllSelected() {
        return this.element.children().length == this.element.children(".selected").length
    }
    
    addElement(element) {
        
        // the new element needs to be ortable as well
        element.addClass("ui-sortable-handle");
        this.element.sortable('refresh');
        this.createHandleEventListeners(element);
    }
    
    
    deleteElement(element) {
        // delete a given item
        
        this.deleteCallback(this, element);
        
        $(element).addClass("deleted")
        .removeClass("selected") // to prevent bugs
        .slideUp();
    }
    
    deleteSelected() {
        // delete selected items
        
        var selected = this.element.children().filter(".selected");
        
        selected.each((index, elem) => this.deleteElement(elem));
        
        // automatically exit selectMode
        this.setSelectMode(false);
    }
    
    createHandleEventListeners(selector) {
        
        let self = this;
        let menu = this.menu;
        
        // mouse interaction with a single handle/image
        
        selector.contextmenu(function(e) {  // show custom context menu (right click)
                self.rightClickElement = $(this);
                self.updateContextMenu(self.rightClickElement);
                menu.show();
                menu.position({my: "left+3 top-3", of:e, collision: "none fit"});
                e.preventDefault();
            }
        )
        .mousedown(function(e) {
            
            if(e.buttons == 1) { // a normal (left) click
                if(self.selectMode) {
                    // click => selecting
                    $( this ).toggleClass("selected");
                    self.selected = $( this ).hasClass("selected");
                    self.selectChangeCallback(self, this);
                } else {
                    // enter select mode if the mouse is hold down (like on a smartphone)
                    self.mousedown_timeout = setTimeout(() => {
                        
                        // trigger mouseup to prevent dragging event
                        $( this ).trigger("mouseup");
                        
                        self.setSelectMode(true);
                        
                        $( this ).toggleClass("selected");
                        self.selected = $( this ).hasClass("selected");
                    }, 300);
                }
            } else if(e.buttons == 4) { // middle mouse for dragging
                
                if(self.selectMode) {
                    self.triggerMultiSort();
                } else {
                    // enable dragging with middle mouse button in normal mode (which is usually bind to the left mouse button)
                    var event = jQuery.Event('mousedown', {
                        which: 1,
                        pageX: e.pageX,
                        pageY: e.pageY,
                    });
                    
                    $(this).trigger(event);
                }
            }
        })
        .mouseover(function(e) { // mass selecting (like on a smartphone)
            if(e.buttons == 1 && self.selectMode) {
                $(this).toggleClass("selected", self.selected);
            }
        });
    }

    createEventListeners() {
        // mouse interaction
        
        let self = this;
        let menu = this.menu;
        
        // hide menu by clicking outside somewhere (like you usually expect it)
        $(document).click(() => self.menu.hide());
        
        // All interactions refer to a single item
        this.createHandleEventListeners(this.element.children())
        
        
        $(document).mouseup(function(e) {
            // prevent the select mode from being entered
            clearTimeout(self.mousedown_timeout);
            
            // automatically exit selectMode
            if(self.selectMode) {
                if(!self.element.children().filter(".selected").length) {
                    self.setSelectMode(false);
                }
            }
            
        });
    }
}

$(function() {
    let button_add = $('#id_images-ADD')
    let button_select = $('#id_images-SELECT')
    let button_unselect = $('#id_images-UNSELECT')
    let button_delete = $('#id_images-DELETE')
    
    
    // TODO do not use #id_images-FORMS !
    var sas = new SelectAndSort(
        "#id_images-FORMS",
        {
            sortUpdate: instance => {
                
                // update all orders according to new sorting
                instance.element.children().each((index, e) => {
                    $('input[name$="-ORDER"]', e).val(index+1)
                })
            },
            selectChange: (instance, element) => {
                button_select.prop("disabled",instance.checkAllSelected())
            },
            selectModeChange: (instance, value) => {
                button_add.prop("disabled",value)
                button_select.prop("disabled",instance.checkAllSelected())
                button_unselect.prop("disabled",!value)
                button_delete.prop("disabled",!value)
            },
            delete: (instance, elem) => {
                $('input[name$="-DELETE"]', elem).val(1);   
            }
        }
    );
    
    button_add.click(() => {
        
        var element = $("#id_images-FORMS").children().last();
        var input_label = element.find("label");
        
        sas.addElement(element);
        
        element.find("input").get(0).addEventListener('change', (e) => {

            // getting a hold of the file reference
            var file = e.target.files[0]; 

            // read the user file 
            var reader = new FileReader();
            reader.readAsDataURL(file);
            
            
            reader.onload = readerEvent => {
                // create an image object from the upload file
                var image = new Image();
                
                image.src = readerEvent.target.result;
                
                input_label.replaceWith(image)
            }

        })

        // clicking on the label opens the file dialog
        input_label.click();
    })
    button_select.click(() => sas.selectAll())
    button_unselect.click(() => sas.unselectAll())
    button_delete.click(() => sas.deleteSelected())
    
    
    // find the input containing the cover id and add the .cover-image class to the correct <li>
    var val = $('#id_cover').val();
    var element = $('input[name$="-id"][value="'+val+'"]')
    element.parents(".ui-sortable-handle").addClass("cover-image")
});
