const adds = [];
var currrent_amount = parseInt(0, 10);
var price_per_day = parseInt($('#estimated_amount').data('price_per_day'));
var start_date;
var end_date;

$(document).ready(
    
    $(document).click(event => {

        // Update total with choosen adds
        if (event.target.type === "checkbox") {
            currrent_amount = parseInt($('#estimated_amount').text(), 10);
             // Add adds to the list
             if (adds.includes(event.target.name)) {
                let index = adds.indexOf(event.target.name);
                adds.splice(index, 1);
                currrent_amount -= parseInt(event.target.value, 10);
            } else {
                adds.push(event.target.name);
                currrent_amount += parseInt(event.target.value, 10);
            }
            
            $('#estimated_amount').text(currrent_amount);
        }

        // Update total with choosen dates
        if (event.target.type === 'date') {
            if (event.target.name === 'details_start_date') {
                $('#details_start_date').change(ev => {
                    if (new Date(ev.target.value) < new Date()) {
                        alert('"Pick-up" date must be at least today.');
                    } else {
                        start_date = new Date(ev.target.value);
                    }
                    
                })
            } 
            if (event.target.name === 'details_end_date') {
                $('#details_end_date').change(ev => {
                    end_date = new Date(ev.target.value);
                    if (end_date <= start_date) {
                        alert('"Pick-up" date must be earlier then "Drop-off"')
                    } else {
                        var diffTime = Math.abs(end_date - start_date);
                        var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                        $('#estimated_amount').text(currrent_amount + price_per_day * diffDays); 
                        $('#estimated_days').text(diffDays);
                        
                        // Update value of hidden total input
                        $('#total').prop("value", (currrent_amount + price_per_day * diffDays))
                    }    
                })
            }  
        }

        // Turn on-off deliver_to and pick_up_from fields
        if (adds.includes('#add_2')) {
            $('#deliver_to').prop('disabled', false)
        } else {
            $('#deliver_to').prop('disabled', true),
            $('#deliver_to').prop('value', '')
        }
        if (adds.includes('#add_3')) {
            $('#pick_up_from').prop('disabled', false)
        } else {
            $('#pick_up_from').prop('disabled', true),
            $('#pick_up_from').prop('value', '')
        }

    })
)