var msg = new SpeechSynthesisUtterance();
var isHalted = false;

window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
const recognition = new window.SpeechRecognition();
recognition.continuous = false;
recognition.interimResults = true;

recognition.onresult = function(event) {
    if (!isHalted) {
        $("#speech-progress").text(event.results[0][0].transcript);
    }
};

recognition.onspeechend = function(event) {
    recognition.stop();
    isHalted = true;

    var bit = $("#speech-progress").text().toLowerCase();
    var hir = wanakana.toHiragana(bit);

    if ('again please'.includes(bit) || 'も一度お願いします'.includes(bit)) {
        setTimeout(repeat, 2000);
    }

    else if ('next please'.includes(bit) || '次に'.includes(bit)) {
        setTimeout(submit, 2000);
    }
    
    else {
        if (
            $('#text-spoiler').text().toLowerCase().includes(bit) ||
            $('#text-subtitle').text().toLowerCase().includes(bit) ||
            $('#text-spoiler').text().includes(hir))
        {
            $("#speech-progress").text(bit + " ✅");
            $('#snd-success')[0].play();
    
            setTimeout(submit, 2000);
        } else {
            $("#speech-progress").text(bit + " ❌");
            $('#snd-fail')[0].play();
    
            powerswap();
            setTimeout(repeat, 2000);
        }
    }
}

function submit() {
    //
    var jso = {
        'jlpt': $('input:radio[name=options]:checked').val(),
        'drct': $('input:radio[name=direction]:checked').val()
        }

    $.ajax({
        url: '/fetch_word',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            update_titles(data['message']);
        },
        data: JSON.stringify(jso)
    });
}

function speak(text,queue=true) {
    
    msg.text = text;

    if ($('input:radio[name=direction]:checked').val() == 0) {
        msg.lang = 'ja-JP';
    } else {
        msg.lang = 'en-US';
    }
    
    msg.rate = 0.9;
    window.speechSynthesis.speak(msg);
}

msg.onend = function() {
    $('#snd-ready')[0].play();
    if ($('input:radio[name=direction]:checked').val() == 0) {
        recognition.lang = 'en-US';
    } else {
        recognition.lang = 'ja-JP';
    }

    try {
        recognition.start();
    }

    catch (error) {
        console.log(error);
    }
    
    isHalted = false;
}

function update_titles(data) {
    if (data[1] != "") {
        $('#text-title').text(data[1].toString());                  
        $('#text-subtitle').text(data[0].toString());
    } else {
        $('#text-title').text(data[0].toString());
        $('#text-subtitle').text("");
    }
    $('#text-spoiler').text(data[3].toString());

    speak(data[1]);
}

function repeat() {
    speak($("#text-title").text(),false);
}

function powerswap() {
    var spoiler = $('#text-spoiler').text();
    var title = $('#text-title').text();
    $('#text-spoiler').text(title);
    $('#text-title').text(spoiler);

    if ($('input:radio[name=direction]:checked').val() == 0) {
        $("#jp")[0].checked = false;
        $("#en")[0].checked = true;
    } else {
        $("#en")[0].checked = false;
        $("#jp")[0].checked = true;
    }
}

$(document).on('click', '.panel div.clickable', function (e) {
    var $this = $(this); //Heading
    var $panel = $this.parent('.panel');
    var $panel_body = $panel.children('.panel-body');
    var $display = $panel_body.css('display');

    if ($display == 'block') {
        $panel_body.slideUp();
    } else if($display == 'none') {
        $panel_body.slideDown();
    }
});

$(document).ready(function(e){
    var $classy = '.panel.autocollapse';
    var $found = $($classy);
    $found.find('.panel-body').hide();
    $found.removeClass($classy);
});