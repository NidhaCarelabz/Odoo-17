/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
console.log(publicWidget, "publicWidget")

$(document).ready(function() {
    $('#meeting_schedule_form').on('submit', function(event) {
        var meetingStart = new Date($('#meeting_start').val());
        var meetingEnd = new Date($('#meeting_end').val());
        var currentTime = new Date();

        if (meetingStart <= currentTime || meetingEnd <= currentTime) {
            event.preventDefault();
            $('#errorMessage').text("Please select a future date and time for both the start and end.").show();
        } else if (meetingStart >= meetingEnd) {
            event.preventDefault();
            $('#errorMessage').text("The end date and time must be later than the start date and time.").show();
        }
    });
});

var MultiSelectTag = publicWidget.Widget.extend({
    selector: '.sales_enquiry_form',
    start: function () {
        var self = this;
        var $servicesSelect = $('#web_sales_enq_services');
        var $servicesValsField = $('#web_sales_enq_services_vals');
        
        function updateSelectField($select, $hiddenField) {
            var selectedValues = $hiddenField.val().split(',');
            $select.val(selectedValues).trigger('change');
        }

        function updateCountryCode() {
            var selectedValues = $('#web_sales_enq_country').find('option:selected').val()
            $('#country_code').val('+' + selectedValues);
        }

        $servicesSelect.on('change', function () {
            var selectedValues = $(this).val();
            console.log("vals >>>>>>>>>", selectedValues);
            $servicesValsField.val(selectedValues);
        });

        if ($servicesValsField.val()) {
            updateSelectField($servicesSelect, $servicesValsField);
        }

        $('#web_sales_enq_country').on('change', updateCountryCode );
        updateCountryCode(); 

        $('.multiple-select-many2many').select2();


    }
});

publicWidget.registry.Many2many_tag = MultiSelectTag;

return MultiSelectTag;