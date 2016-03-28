$(document).ready(function() {
    //map select    
    $('.lake-map:not(:first)').hide();
    $('#map-select').change(function(){
        $('.lake-map').hide(); 
        $(this.value).show();
    });
    
    //slideshow 
    var current = 1;
    var numphotos = $('.lake-photo').length;
    $('#numphotos').html(current + '/' + numphotos); 
    $('#next').click(function(){
        $('.lake-photo:nth-child('+current+'').hide();
        current +=1; 
        if(current > numphotos) current -= numphotos;
        $('.lake-photo:nth-child('+current+'').show();
        $('#numphotos').html(current + '/' + numphotos); 
    });
    $('#previous').click(function(){
        $('.lake-photo:nth-child('+current+'').hide();
        current -= 1; 
        if(current < 1) current += numphotos;
        $('.lake-photo:nth-child('+current+'').show();
        $('#numphotos').html(current + '/' + numphotos); 
    });
});
