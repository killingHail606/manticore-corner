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

try {
	document.querySelector('.tabs').onclick = function (event) {
		let target = event.target;
		if (target.className == 'section') {
			for (let i = 0; i < tab.length; i++) {
				if (target == tab[i]) {
					showTabsContent(i);
					break;
				}
			}
		}
	}
} catch (e) {}

function showTabsContent(b){
	if(tabContent[b].classList.contains('hide')){
		hideTabsContent(0);
		tab[b].classList.add('section-checked');
		tabContent[b].classList.remove('hide');
		tabContent[b].classList.add('show');
	}
}

try {
	let form_label = document.querySelector('#update_avatar_form label');
	let button = document.querySelector('#id_picture')
	button.addEventListener('change', () => {
		let oFile = button.files[0];
		form_label.innerText = oFile['name'];
	});
} catch (e) {}

let nick = '';

try {
	let textarea = document.querySelector('#new_comment');
	let button_send = document.querySelector('.comment_button')

	function answer(num_com, username) {
		button_send.setAttribute('data-answer', num_com)
		textarea.value = `${username}, `;
		textarea.focus();
		nick = username;
	}

	textarea.addEventListener('input', () => {
		if (nick !== textarea.value.split(',')[0]) {
			button_send.removeAttribute('data-answer');
		}
	})
} catch (e) {}


function go_to_comment(id_comment) {
	let comment_block = document.querySelector(`#num-com-${id_comment}`);
	let top_px = window.pageYOffset + ((comment_block.getBoundingClientRect().top + document.body.scrollTop) - 200);
	window.scrollTo(0,top_px)

	try {
		document.querySelector('.found-answer').classList.remove('found-answer');
	} catch (e) { }

	comment_block.classList.add('found-answer');
}





