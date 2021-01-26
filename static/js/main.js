function search_show() {
    let search_input = document.querySelector('.upper_header .wrapper .buttons .search form #id_body');
    let search_button = document.querySelector('.upper_header.flex-center .buttons .search button');
    let search_hide = document.querySelector('.upper_header.flex-center .buttons .search .search_hide');
    let search_show = document.querySelector('.upper_header.flex-center .buttons .search .search_show');

    search_show.style.display = 'none';
    search_input.style.display = 'inline';
    search_button.style.display = 'inline';
    search_hide.style.display = 'inline';
}

function search_hide() {
    let search_input = document.querySelector('.upper_header .wrapper .buttons .search form #id_body');
    let search_button = document.querySelector('.upper_header.flex-center .buttons .search button');
    let search_hide = document.querySelector('.upper_header.flex-center .buttons .search .search_hide');
    let search_show = document.querySelector('.upper_header.flex-center .buttons .search .search_show');

    search_show.style.display = 'inline';
    search_input.style.display = 'none';
    search_button.style.display = 'none';
    search_hide.style.display = 'none';
}

function menu_show() {
	let menu = document.querySelector('.menu-mobile')
	console.log(menu)

	menu.style.display = 'flex';
}

function menu_hide() {
	let menu = document.querySelector('.menu-mobile')

	menu.style.display = 'none'
}

let tab;
let tabContent;

window.onload = function(){
	tabContent = document.getElementsByClassName('rules');
	tab = document.getElementsByClassName('section');
	hideTabsContent(1);
}

function hideTabsContent(a){
	for(let i = a; i < tabContent.length; i++){
		tabContent[i].classList.remove('show');
		tabContent[i].classList.add('hide');
		tab[i].classList.remove('section-checked');
	}	
}

document.querySelector('.tabs').onclick = function(event){
	let target = event.target;
	if(target.className == 'section'){
		for(let i = 0; i < tab.length; i++){
			if(target == tab[i]){
				showTabsContent(i);
				break;
			}
		}
	}
}

function showTabsContent(b){
	if(tabContent[b].classList.contains('hide')){
		hideTabsContent(0);
		tab[b].classList.add('section-checked');
		tabContent[b].classList.remove('hide');
		tabContent[b].classList.add('show');
	}
}


