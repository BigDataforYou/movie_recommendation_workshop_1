movie_indexes = []
checked = [0,0,0,0,0,0,0,0,0,0,0,0]
current_movie = ''

    function merge_objects(obj1,obj2){
    var obj3 = {};
    for (var attrname in obj1) { obj3[attrname] = obj1[attrname]; }
    for (var attrname in obj2) { obj3[attrname] = obj2[attrname]; }
    return obj3;
    }
    
    function first(obj){
            for (var first in obj) return first
    }

    function display_current_recommendation_settings(settings){
            console.log('1' + settings)
            console.log(settings.genre_settings)
            console.log(settings.decade_settings)
            let tmp_settings = merge_objects(settings.genre_settings, settings.decade_settings)
            let tmp_html = ''
            console.log('2' + tmp_settings)
            for(var setting in tmp_settings){
                console.log(setting)
                    tmp_html += "<div class='recommendation_value_class'><div class='r_v_column'><span class='r_v_text_style'>" + setting
                    tmp_html += "</span></div><div class='r_v_column'><span class='r_v_text_style'>" + tmp_settings[setting].toFixed(2)
                    tmp_html += "</span></div></div>"
            }
            /*for(decade in settings.decade){
                    tmp += "<div class='recommendation_value_class'*/
            console.log('3' + tmp_html)
            $("#user_preferences").html(tmp_html);
    }

    function display_suggested_movie(data){
            current_movie = data.id
            let tmp_html = ''
            tmp_html += "<div class='preset_movies'><div class='movie_box'><div class='movie_box_title'>"
            tmp_html += "<span class='movie_text_suggested_style'>" + data.title + "&nbsp&nbsp" +  data.genre +"</span></div></div></div>"
            $("#new_movie_suggested_box").html(tmp_html)
    }

    function toggle_movie(id){
        if( $("#box_"+id).data('checked' == 1) ){
                $('#box_' + id).css('background-color',  'aqua')
                $('#box_' + id).data('checked', '0')
        }
        else{
                $('#box_' + id).css('background-color', 'grey')
                $('#box_' + id).data('checked', '1')
        }
       
        checked[id] = 1
    }

$(function(){

    $("#like").click(function(){
        $.get("initialize/1/" + current_movie, 
                function(data){
                        display_suggested_movie(JSON.parse(data))
                        display_current_recommendation_settings(JSON.parse(data))
                });
    });

    $("#dislike").click(function(){
        $.get("initialize/-/" + current_movie, 
                function(data){
                        display_suggested_movie(JSON.parse(data))
                        display_current_recommendation_settings(JSON.parse(data))
                });
    });

    function get_movie_indexes(data){
            for(hh in data) movie_indexes.push(first(data[hh]))
    }

    function init_movies(data){
        let count = 0
        for(j=0;j<2;j++){
            let tmp_html = ''
            for(i=0;i<6;count++, i++){
                tmp_html += "<div class='preset_movies'><div id='box_" + count + "' class='movie_box' onClick='toggle_movie(" + count + ")'>"
                tmp_html += "<div class='movie_box_title'><span class='movie_text_style' id='movie_" + count + "'>"
                tmp_html += " " + data[count][first(data[count])] + "</span></div></div></div>"
            }
            if(j==0)
                $("#first_row").html(tmp_html)
            else
                $("#second_row").html(tmp_html)
        }
    }

    //initializei
    $.ajax({
        url: 'http://localhost/init/', 
        dataType:'json',
        success: function(data){
            get_movie_indexes(data)
            init_movies(data)
        },
        error: function(data){
            alert('error')
        }
    });
    
    
    
    $("#btn_reset").click(function(){
        location.reload()
    });
    
    $("#btn_start").click(function(){
          $.ajax({
                  url:"initialize/" + checked.join('') + "/" + movie_indexes.join('-'),
                  success: function(data){
                            display_suggested_movie(JSON.parse(data))
                  }
                  
          });
    })
})
