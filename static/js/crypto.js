
console.log('yo crypto js');
$('#crypto_curr_select').change(
    function changeCurrencyCrypto(){

            console.log('changing curr js');
            let alpha_3 = this.value;
            console.log(alpha_3);
            if (alpha_3){
                $.ajax({
                type: 'POST',
                url: '/crypto/change_currency/',
                data: {
                    currency_code: alpha_3,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function(){
                    window.location.reload(true);
                },
                error: function(){
                    console.log('change curr js error');
                }
            }
        )};
    }
);




