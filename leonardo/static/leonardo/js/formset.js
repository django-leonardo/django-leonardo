/* For dynamically adding/deleting Django inline formsets
 * Original snippet from: https://djangosnippets.org/snippets/1389/
 * Original snippet by: elo80ka
 * This version by: halfnibble (Josh Wedekind)
 * Updated 5/13/2015
 */

var Formset = (function() {
    var callbacks = {},
        empty_form = {},
        form_count = 0,
        form_manager = {},
        form_placeholder = $('#formset-placeholder')[0],
        form_selector = '.dynamic-form',
        prefix = 'formset';        

    function setup(context) {
        /***************************************
         * Common context attributes           *
         *   prefix:           'formset'       *
         *   form_selector:    '.dynamic-form' *
         *   form_placeholder: DOM.element     *
         *   callbacks:        { funcs... }    *
         ***************************************/
        $.extend(this, context);

        // Set a few more attributes
        this.form_manager = $('#id_' + this.prefix + '-TOTAL_FORMS');
        this.form_count = parseInt(this.form_manager.val());        
        if (this.form_placeholder === undefined || this.form_placeholder === [])
            this.form_placeholder = $('#' + this.prefix + '-placeholder');

        // Setup the empty form for add_form()
        var empty_form = $(this.form_selector + ':first').clone(true).get(0);
        // Clear all values except for hidden field values.
        $(empty_form).find(':input')
            .removeAttr('checked')
            .removeAttr('selected')
            .not(':button, :submit, :reset, [type="hidden"], :radio, :checkbox')
            .val('')
            .attr('value',''); // Handle UpdateView default values
        this.empty_form = empty_form;

        if (this.callbacks.setup)
            this.callbacks.setup(this);
    }

    function add_form() {
        var self = this;

        // Assume new forms get last index counter
        var index = this.form_count;
        console.log(form);
        // Create form to add
        var form = $(this.empty_form).clone(true).get(0);
        console.log(form);
        this.update_index(form, index, false);
        
        // Add form after last one, or after the placeholder if none exist.
        if ($(this.form_selector + ':last').length > 0)
            $(form).insertAfter(
                $(this.form_selector + ':last')
            );
        else
            $(form).insertAfter(this.form_placeholder);

        // Update all pertinent form field indexes
        $(form).children('.hidden').removeClass('hidden');
        $(form).find('div, input, select, label, button').each( function() {
            self.update_index(this, index, false);
        });

        // Update index counter
        ++this.form_count;
        this.form_manager.val(this.form_count);

        if (this.callbacks.add_form)
            this.callbacks.add_form(this, form, index);

        return false;
    }

    function delete_form(button) {
        var self = this;
        $(button).parents(this.form_selector).hide(400, function() {
            var form = this;
            $(form).remove();
            --self.form_count;
            self.form_manager.val(self.form_count);

            // Delete anything else before updating
            if (self.callbacks.delete_form)
                self.callbacks.delete_form(self, form);

            // Update all formset indexes, etc.
            self.update_all();
        });

        return false;
    }

    function update_all() {
        var self = this;
        // Get list of all forms in formset
        var forms = $(this.form_selector);

        for (var index = 0; index < this.form_count; index++) {
            /*jshint loopfunc: true */
            var form = forms.get(index);

            // Update form index, then all pertinent field indexes
            this.update_index(form, index);
            $(form).find('div, input, select, label, button')
                .each( function() { self.update_index(this, index); });

            if (this.callbacks.update_all)
                this.callbacks.update_all(this, form, index);
        }
    }

    function update_index(element, index, external_links) { 
        if (external_links === undefined)
      external_links = true; // Default: update links to element ID
        var regex = new RegExp('(' + this.prefix + '-\\d+)');
        var replacement = this.prefix + '-' + index;

        if ($(element).attr("for"))
            $(element).attr(
                "for",
                $(element).attr("for")
                .replace(regex, replacement)
            );
        if (element.id) {
            // Update targets to element
            if (external_links === true)
                $('a[href="#'+element.id+'"]').attr('href', function (i, attr) {
                    return attr.replace(regex, replacement);
                });
            element.id = element.id.replace(regex, replacement);
      }
        if (element.name)
            element.name = element.name.replace(regex, replacement);
        if (element.getAttribute('data-prefix'))
            element.setAttribute(
                'data-prefix',
                element.getAttribute('data-prefix')
                .replace(regex, replacement)
            );

        // Use if you want to replace more field attributes
        // E.g. element.className
        if (this.callbacks.update_index)
            this.callbacks.update_index(this, element, index,
                                        regex, replacement);
    }

    return {
        // Properties
        callbacks: callbacks,
        empty_form: empty_form,
        form_count: form_count,
        form_manager: form_manager,
        form_placeholder: form_placeholder,
        form_selector: form_selector,
        prefix: prefix,
        // Methods
        setup: setup,
        add_form: add_form,
        delete_form: delete_form,
        update_all: update_all,
        update_index: update_index
    };
});