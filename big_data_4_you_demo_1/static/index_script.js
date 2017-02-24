$(function(){

    function checked_films(){
            var check_list = '';
            for(var i=0;i<11;i++){
                    var flag = $("#cmn-toggle-" + i).prop('checked') ? 1 : 0;
                    check_list += flag;
            }
            return check_list;
    }

    /*movie_id = data.split(' ')[0];
     * data = data.split('Name')[0].slice(5);*/
    $("#reset").on("click", function(){
            document.location.reload(true);
    });

    $("#proceed").on("click", function(){ 
            flags = checked_films();
            indexes = movie_list;
           $.get(
                "initialize/" + flags + '/' + indexes,
                function(data){
                        
                        create_dialog(data);

                }
            );
    });
    tmp_response = '';
    function create_dialog(data){
            $("#movie_ask").html("<span class='ui-icon ui-icon-alert' style='float:left; margin:12px; 12px 20px 0;'></span>" + data.split('Name')[0].slice(5));
            $( "#dialog-confirm" ).dialog({
                    resizable: false,
                    height: "auto",
                    width: 400,
                    modal: true,
                    buttons: {
                            "YES": function() {
                                $.get(
                                     "initialize/1/" + data.split(' ')[0],
                                        function(response){
                                            //alert("response yes");
                                            tmp_response = response;
                                            setTimeout( function(){
                                                    create_dialog(tmp_response);
                                            },100);
                                            $(this).dialog("close");
                                            
                                        });    
                            },
                            "NO": function() {
                                    $.get(
                                         "initialize/-/" + data.split(' ')[0],
                                         function(response){
                                               //alert("response no");
                                               tmp_response = response;
                                               setTimeout( function(){
                                                            create_dialog(tmp_response)
                                               }, 100);
                                                $(this).dialog("close");
                                         });
                            }
                    }
            });
    }


});
