$(function(){
	fox.navigator.toggleCheckbox("genre");
	fox.navigator.toggleCheckbox("quality");
	fox.navigator.toggleCheckbox("voice");

	$(document).on("click", 'body', function() {
		fox.navigator.openSelect();
	});

});

if(typeof(fox)=='undefined') fox={};

fox.navigator = {
	selectTimer: null,
	updateTimer: null,
	lastRequest: null,
	selectBlockClose: null,
	requestUpdate: false,

	showPopup: function(number, num, href) {
		if( number > 0 ) {
			$("#filtersearch").removeAttr('disabled').find("#btntextfilter").html("ÐÐ°Ð¹Ð´ÐµÐ½Ð¾ ("+num+")");

			$('#filtersearch').unbind('click').click(function() {
				if( fox.navigator.requestUpdate ) {
					return false;
				}

				$('#filterload').show();

				fox.navigator.requestUpdate = true;

				if( $.browser.mobile || $(document).width() < 1000 ) {
					window.location.href = href;
				} else {
					$.ajax({url: href, method: "POST", dataType: "json", data: {is_ajax: 1}, success: function (data) {
						if( data.status == 'ok' ) {
							if( data.html.length ) {
								for ( var i=0; i<data.html.length; ++i ) {
									if( data.html[i].el && $(data.html[i].el).length ) {
										$(data.html[i].el).html( data.html[i].html );
									}
								}
							}

							if( !$('body').hasClass('filter') ) {
								$('body').addClass('filter')
							}

							$(".sortn-box").show();
							$("time.ago").timeago();

							if ($.cookie('kp_wrapper') == 'grid') {
								$('.btn-grid').addClass("active");
								$('.btn-list').removeClass("active");
							} else {
								$('.btn-list').addClass("active");
								$('.btn-grid').removeClass("active");
							}

							history.pushState({page: href}, null, href);
							$('#filterload').fadeOut(300);
						}
						fox.navigator.requestUpdate = false;
					}});
				}
				return false;
			});
		} else {
			$("#filtersearch").attr('disabled', 'disabled').find("#btntextfilter").html("ÐÐ¸Ñ‡ÐµÐ³Ð¾ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð¾");

			$("#filtersearch").unbind('click').click(function(){
				fox.navigator.requestUpdate = false;
				return false;
			});
		}
	},

	blockSelect: function(){
		fox.navigator.selectBlockClose = true;
		fox.navigator.selectTimer = setTimeout(function(){fox.navigator.selectBlockClose=false},200);
	},

	openSelect: function(selector){
		if(!fox.navigator.selectBlockClose){
			fox.navigator.selectBlockClose = true;

			fox.navigator.selectTimer = setTimeout(function(){
				fox.navigator.selectBlockClose = false;
			}, 100);

			if( selector ){
				if( $("#"+selector).css("display") == 'block' ) {
					$("#" + selector).hide();
				} else {
					$("#" + selector).show();
				}
				$(".selectList:not(#"+selector+")").hide();
			} else {
				$(".selectList").hide();
			}
		}
	},

	toggleCheckbox: function(type, selector, obj){

		if( obj ) {
			$all = $(obj).parents(".selectList").find("." + type + "_" + $(obj).val() + " input");
			$all.prop("checked", $(obj).prop('checked'));

			if( !obj.checked ){
				$all.parents(".selectItem").removeClass("act");
			} else {
				$all.parents(".selectItem").addClass("act");
			}
		}

		var itemList = [];
		var itemCount = 0;
		var itemListUnique = [];

		$("#" + type + "List input:checked").each(function(){
			if( !itemListUnique[$(this).val()] ){
				itemList[itemList.length] = $(this).attr("data-name");
				itemListUnique[$(this).val()] = $(this).val();
				itemCount++;
			}
		});

		var Selects = [];
		Selects["genre"] = "Выбрать жанр";
		Selects["quality"] = "Выбрать год";
		Selects["voice"] = "Убрать жанры:";

		$("#" + type + "ListTitle").html(Selects[type] + (itemCount ? " ("+itemCount+")" : ""));

		if( itemCount ) {
		//	$("#" + type + "ListTitles_and .list").html(itemList.join(", "));
			$("#" + type + "ListTitles_and").fadeIn();
		} else {
		//	$("#" + type + "ListTitles_and .list").html("");
			$("#" + type + "ListTitles_and").fadeOut();
		}

		if( itemCount > 0 ){
		//	$("#" + type + "ListTitles_or .list").html(itemList.join(", "));
			$("#" + type + "ListTitles_or").fadeIn();
		} else {
		//	$("#" + type + "ListTitles_or .list").html("");
			$("#" + type + "ListTitles_or").fadeOut();
			$("#" + type + "ListTitles_and input").prop("disabled", false);
			$("#" + type + "ListTitles_or input").prop("checked", false);
		}

        if( itemCount > 0 ) {
            $("#ListTitles_block").fadeIn();
        }
	},

	toggleCheckboxOff: function(type, obj) {
		if( obj && obj.checked ) {
			switch (type) {
				case 'is_film': $("#is_serial").prop("checked", false); break;
				case 'is_serial': $("#is_film").prop("checked", false); break;
			}
		}
	},

	setRadioBox: function(type) {
		if( type ) {
			$("#" + type).attr({checked: true}).prop("checked", true);
			var minObjects = ["sort_rating", "sort_kp", "sort_imdb"];
			if( minObjects.indexOf( type ) != -1 ) {
				$(".bestMoviesNav").find('#votepeople_block').fadeIn();
			} else {
				$(".bestMoviesNav").find('#votepeople_block').fadeOut();
			}
		}
	},

	syncronizeYears: function(Start, End, Source){
		if(!years) {
			years = [$("#start_year").val(), $("#end_year").val()];
		}

		Start = parseInt(Start,10);
		End = parseInt(End,10);

		if(Start < 1890 || Start > 2016 || End < 1890 || End > 2020) {
			return false;
		}

		if(!Start) Start = years[0];
		if(!End) End = years[1];

		if(years[0] != Start && End < Start) {
			End = Start;
		}

		if(years[1] != End && End < Start ) {
			Start = End ;
		}

		if(years[0] != Start && End - Start > 10) {
			End = Start + 10;
		}
		if(years[1] != End && End - Start > 10) {
			Start = End - 10;
		}

		$("#yearrange").slider( "values", 0, Start );
		$("#yearrange").slider( "values", 1, End );
		$("#start_year").val(Start);
		$("#end_year").val(End);

		if( Source == 'start_year' || Source == 'end_year' ){
			$("#years_list").val('');
			$("#years_decade_list").val('');
		}

		fox.navigator.update();
		years = [ Start, End ];
		return years;
	},

	validateInterval: function(type, what, max, min, obj){
		if(obj.value == '') {
			return;
		}
		val = obj.value.replace(',','.').replace(/[^\d\.]/g,'');
		val_ar = val.split(".");
		val = val_ar[0] + (val.indexOf(".") > 0 ? "." + val_ar[1] : "");
		val = isNaN(parseFloat(val)) ? min : val;
		normVal = Math.max(min, Math.min(val , max));
		val = parseFloat(val) != normVal ? normVal : val;
		obj.value = val;
		if(type == 'min'){
			if(parseFloat(val) > $("#"+what+"_max").val()) {
				$("#"+what+"_max").val(val);
				$("#"+what+"range" ).slider( "values" , 1 , val );
			}
			$( "#"+what+"range" ).slider( "values" , 0 , val );
		} else {
			if(parseFloat(val) < $("#"+what+"_min").val()) {
				$("#"+what+"_min").val(val);
				$("#"+what+"range" ).slider( "values" , 0 , val );
			}
			$( "#"+what+"range" ).slider( "values" , 1 , val );
		}
		fox.navigator.update();
	},

	clearRange : function(name){
		var min_field = $( "#"+name+"_min" ).get(0);
		var max_field = $( "#"+name+"_max" ).get(0);
		max_field.value = max_field.defaultValue;
		min_field.value = min_field.defaultValue;
		$( "#"+name+"range" ).slider("values", 1, max_field.value);
		$( "#"+name+"range" ).slider("values", 0, min_field.value);
		fox.navigator.update();
	},

	clearForm: function(){
		fox.navigator.requestUpdate = true;
		fox.navigator.toggleCheckbox("genre");		
		fox.navigator.toggleCheckbox("quality");		
		fox.navigator.toggleCheckbox("voice");
		fox.navigator.serializeForm();
		fox.navigator.requestUpdate = false;
		fox.navigator.update();
	},

	serializeForm: function(serialize_folders){
		var data = $(".bestMoviesNav").serializeObject();

		var rangeObjects = ["years"];

		for(var p in rangeObjects) {
			if( data['m_act['+rangeObjects[p]+'][min]'] ) {
				$("select[name='m_act["+rangeObjects[p]+"][max]'] option").each(function() {
					if( $(this).val() && data['m_act['+rangeObjects[p]+'][min]'] > $(this).val() ) {
						$(this).hide();
					} else {
						$(this).show();
					}
				});
			} else {
				$("select[name='m_act["+rangeObjects[p]+"][max]'] option").show();
			}

			if( data['m_act['+rangeObjects[p]+'][max]'] ) {
				$("select[name='m_act["+rangeObjects[p]+"][min]'] option").each(function() {
					if( $(this).val() && data['m_act['+rangeObjects[p]+'][max]'] < $(this).val() ) {
						$(this).hide();
					} else {
						$(this).show();
					}
				});
			} else {
				$("select[name='m_act["+rangeObjects[p]+"][min]'] option").show();
			}

			if(data['m_act['+rangeObjects[p]+'][min]'] && data['m_act['+rangeObjects[p]+'][max]'] && parseInt(data['m_act['+rangeObjects[p]+'][min]'], 10) > parseInt(data['m_act['+rangeObjects[p]+'][max]'], 10) ){
				data['m_act['+rangeObjects[p]+'][max]'] = null;
				$("[name='m_act["+rangeObjects[p]+"][max]']").val("");
			}

			var max = data['m_act['+rangeObjects[p]+'][max]'];
			var min = data['m_act['+rangeObjects[p]+'][min]'];

			data['m_act['+rangeObjects[p]+'][max]'] = null;
			data['m_act['+rangeObjects[p]+'][min]'] = null;

			if(max || min) {
				data['m_act[' + rangeObjects[p] + ']'] = (min ? min : '') + ":" + (max ? max : '');
			}
		}

		var arrayObjects = ["quality", "genre", "country", "collect", "voice"];

		for(var p in arrayObjects){
			if(data['m_act['+arrayObjects[p]+'][]'] && (typeof(data['m_act['+arrayObjects[p]+'][]'])=='array' || typeof(data['m_act['+arrayObjects[p]+'][]'])=='object') ){
				data['m_act['+arrayObjects[p]+']'] = data['m_act['+arrayObjects[p]+'][]'].join(",");
			} else if(data['m_act['+arrayObjects[p]+'][]'] && (typeof(data['m_act['+arrayObjects[p]+'][]'])=='string') ){
				data['m_act['+arrayObjects[p]+']'] = data['m_act['+arrayObjects[p]+'][]'];
			}
		}

		var minObjects = ["rating", "kp", "imdb"];

		if( minObjects.indexOf(data['m_act[sort]']) != -1 ) {
			$(".bestMoviesNav").find('#votepeople_block').fadeIn();
		} else {
			$(".bestMoviesNav").find('#votepeople_block').fadeOut();
		}

		return this.trimArray(data);
	},

	trimArray: function(array){
		var rets = {};
		if(typeof(array) == "array" || typeof(array) == "object"){
			for(var k in array){
				var newval = this.trimArray(array[k]);
				if( newval ) {
					rets[k] = this.trimArray(array[k]);
				}
			}
			return rets;
		} else {
			return array;
		}
	},

	update: function(){
		clearTimeout(fox.navigator.updateTimer);
		fox.navigator.updateTimer = setTimeout(function(){
			var request = fox.navigator.serializeForm(true);

			if(JSON.stringify(fox.navigator.lastRequest) == JSON.stringify(request)) {
				return;
			}

			$.post(api_root + "search", request, function(res){
				fox.navigator.lastRequest = request;
				fox.navigator.showPopup(res["number"], res["num"], res["link"]);

				if( res["link"] ) {
					fox.navigator.link = '/' + res["link"] + '/';
				}
			}, 'json');
		}, 100);
	}
}

$.fn.serializeObject = function() {
	var o = {};
	var a = this.serializeArray();
	$.each(a, function() {
		if (o[this.name]) {
			if (!o[this.name].push) {
				o[this.name] = [o[this.name]];
			}
			o[this.name].push(this.value || '');
		} else {
			o[this.name] = this.value || '';
		}
	});
	return o;
};

function isNumber(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
}
