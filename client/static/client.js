/*
	Code referrence from jquery.com
*/

const apiUrl = 'http://localhost:5000';
const apiRoot = '/shareit/api';
const apiU = apiUrl + apiRoot;
const PLAINJSON = "application/json";

const weatherApiRoot = 'http://api.openweathermap.org/data/2.5/weather?';
const weatherApiKey = '7efc67849ce59293818aa1ce2af7a07d';
const weatherApiCity = 'oulu,fi';
const weatherQuery = 'units=metric&q=' + weatherApiCity + '&appid=' + weatherApiKey;
const wetherApiUrl = weatherApiRoot + weatherQuery;


$(document).ready(function() {
    
    /*
        Code structure followed from jstricks.com
    */
	const xhrTimeout = 3000;
	const $containerControls = $('.container.controls');
    const $contentData   = $('.content-data');
    const $controlsData  = $('.controls-data');
    const $formData  = $('.form-data');
    const $weatherData  = $('.weather-data');
    const $homeData  = $('.home-data');
    const $allPosts  = $('.row.posts');
	
	function handleSearchRoute(){
		console.log('search route');
		return;
	}
	
	function handleHomeRoute(){
		console.log('search route');
		return;
	}
	
	if ( window.location.hash ) {
		const cHash = getCurrentHash();
		if( cHash != 'home' ){
			getResource( getCurrentHash() );
			return;
		}
        renderPostsForHomePage();
    }
	
	$(window).on('hashchange', function(e) {
		
			
        // Getting the current hash value
        const cHash = getCurrentHash();
		console.log(cHash)
		getWeatherParams();
		console.log('.. route');
		if(cHash == 'search'){
			console.log('search route');
			return;
		}else if( cHash == 'home' ){
			renderPostsForHomePage();
			$homeData.show(1);
			$containerControls.hide(1);
			return;
		}
		
		$homeData.hide(1);
		$containerControls.show(1);
        getResource();
		
		
    });	
	
	
	/*
		Converts timestamp to understandable time format. 
	*/
	function time(s) {
		return new Date(s * 1e3).toISOString().slice(-13, -5);
	}
	
	/*
	*	Implementation of a different API. 
	*	
	*	OpenWeatherMap API
	*	
	*/
	
	/*
		Gets latest weather data. 
	*/
	function getWeatherParams(){
		$.ajax({
            timeout: xhrTimeout,
            type: 'GET',
            url: wetherApiUrl,
        })
        .done(renderWeatherData)
        .fail(handleAjaxError)
	}
	
	/*
        Code borrowed from stackoverflow
		Converts wind degree to direction. 
	*/
	function degToCompass(num){
		
		var val = Math.floor((num / 22.5) + 0.5);
		var arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
		return arr[(val % 16)];
		
	}
	
	/*
		Renders weather data . 
	*/
	function renderWeatherData(data){
		const city = data.name;
		const main = data.main;
		const wind = data.wind;
		const weather = data.weather;
		const sys = data.sys;
		
		const sunrise = time(sys.sunrise);
		const sunset = time(sys.sunset);
		
		let html = '<div class="row">';
		
		html += '<div class="col s1"><h5> ' + city + '</h5><h4> ' + data.sys["country"] + '</h4></div>';
		
		html += '<div class="col s2">';
		html += '<h5>Hello,</h5><h6>Weather condition : ' + weather[0].main + '</h6>';		
		html += '</div>';
		
		html += '<div class="col s3">'
		html += '<h3> <i class="wi wi-sunrise"></i> <i class="wi wi-sunset"></i></h3>'		
		html += '<p>Sunrise at ' + sunrise + '</p>';
		html += '<p>Sunset is at ' + sunset + '</p>';
		html += '</div>';
		
		html += '<div class="col s3">'
		html += '<h3> <i class="wi wi-humidity"></i> <i class="wi wi-celsius"></i></h3>'
		html += '<p> Humidity: ' + main.humidity + '</p>';
		html += '<p>Temperature: ' + main.temp + '</p>';
		html += '</div>';
		
		html += '<div class="col s2">'
		html += '<h3> <i class="wi wi-day-light-wind"></i> <i class="wi wi-celsius"></i></h3>'
		html += '<p>Wind speed: ' + wind.speed + '</p>';
		html += '<p>Wind deg: ' + wind.deg + '</p>';
		html += '</div>';
		
		html += '</div>';
		
		$weatherData.html( html );
	}
	
	getWeatherParams();
	
	
	/*
	*	Render posts data
	*/
	
	function renderPostsForHomePage(){
		
		
		$.ajax({
            timeout: xhrTimeout,
            type: 'GET',
            url: apiU + '/posts',
        })
        .done(function(data) {
			const items = data["items"];
			let html = '';
            
			// Render all posts data 
			for (item in items) {
				html += '<div class="col s12 m3"> <div class="card blue-grey darken-1"> <div class="card-content white-text">';
				
				html += '<span class="card-title">' + items[item].title + '</span>'
				html += '<p>' + items[item].details.substring(0, 12) + '</p>'		
				html += '</div>';
				html += '<div class="card-action"> <a href="#posts">More</a>';				
				html += '</div></div>  </div>';
			}
			$allPosts.html( html );
			
        })
        .fail(handleAjaxError)
		
	}
	
	
	
	
	
	
	
	
	/**
     * Create a form out of template
     */
    function createForm(adata, resource, method) {
		var formTitle = formatTitle( getCurrentHash() );
		let html = `<h3>${ formTitle } - ${ method }</h3>`;
		const fhref = apiU + getCurrentHash();
		
		
        html += `
                <p>Please note that all fields marked with an asterisk (*) are required.</p>
                <form
                    class="resource-form"
                    data-href="${resource + '/'}"
                    data-method="${escapeAttr(method)}">
            `;
		
        //adata = JSON.parse(adata);

        for (key in adata.data) {
			
			const properties = adata.data[key];
			const name = properties.name;
			
            const title = formatTitle(properties.name);
			const isInteger = false;
            const isRequired = properties.required;

            html += `
                    <label>
                        ${escapeHtml(title)}
                        ${isRequired ? '*' : ''}
                        <br>
                        <input
                            class="u-full-width"
                            name="${name}"
                            type="${isInteger ? 'number' : 'text'}"
                            placeholder="${escapeAttr(properties.prompt)}"
                            ${isRequired ? 'required' : ''}>
                    </label>
                `;
        }

        html += '<br><input class="btn waves-effect waves-light" type="submit" value="Submit">';
        html += '</form>';
        return html;
    }
	
	/*function generateForm(data, resource, method) {
        $contentData.html(createForm(data, resource, method));
    }*/
	
	function renderForm(data, resource, method) {
        $formData.html(createForm(data, resource, method));
    }
	
	/**
     * Load a schema associated with a PATCH, POST or PUT resource and render
     * a form based on the schema.
     */
    function loadSchema(resource, method, schemaUrl) {
        //$resourceInput.prop('disabled', true);

        // Read schema using GET
        $.ajax({
            timeout: xhrTimeout,
            type: 'GET',
            url: schemaUrl,
        })
        .done(function(data) {
			const schema = cachedData["template"];
            renderForm(schema, resource, method);

            // Fill the form with current data if applicable, i.e. when
            // modifying an existing record
            if (cachedData) {
                loadFormData(data);
            }
        })
        .fail(handleAjaxError)
    }
	
	
	function loadFormData(data) {
        const $form = $formData.find('.resource-form');
		
        for (key in data) {
            const mdata = data[key];
            $form.find(`input[name="${key}"]`).val(mdata);
        }
    }	
	
	 /**
     * Load a resource using AJAX when clicking a link with class 'resource-link'.
     */
    $(document).on('click', '.resource-link', function(event) {
        
		event.preventDefault();

        const $this  = $(this);
        const href   = $this.attr('href');
        const method = $this.data('method') || 'GET';

        if (method === 'DELETE' && !confirm('Do you really want to delete this record?')) {
            return;
        }

        if (['PATCH', 'POST', 'PUT'].includes(method)) {
            loadSchema(href, method, $this.data('schema-url'));
            return;
        }		
		
        getResource(href, method);
        
    })

    /**
     * Handle submitting a form built for a PATCH, POST or PUT method.
     */
    .on('submit', '.resource-form', function(e) {
        e.preventDefault();

        const $this = $(this);
        let data = {};

        $this.find('input[type!="submit"]').each(function() {
            const $input = $(this);
            const name = $input.attr('name');
            let value = $input.val();

            if (value === '') {
                return;
            }

            if ($input.attr('type') === 'number') {
                value = parseInt(value, 10);
            }
			
			console.log(name)

            data[name] = value;
        });
		
		
        getResource(
            $this.data('href'),
            $this.data('method'),
            JSON.stringify(data)
        );
		
		return false;
    })
	
	.on('click', '.add-resource', function(e) {
		$.ajax({
            timeout: xhrTimeout,
            type: 'GET',
            url: $(this).data('href'),
        })
        .done(function(data) {
			const fhref = getCurrentHash();
			$formData.html(createForm( data['template'], fhref, 'POST') );
        })
        .fail(handleAjaxError)
		
		
		
	})
    /**
     * Sort table rows when clicking a table heading.
     */
    .on('click', 'thead th', function(e) {
        const $this  = $(this);
        const index  = $this.index();
        const $tbody = $this.closest('table').find('tbody');

        const currentSort = $this.attr('data-tablesort');
        $this.attr('data-tablesort', currentSort === 'asc' ? 'desc' : 'asc');
        $this.siblings().each(function() {
            $(this).removeAttr('data-tablesort');
        });

        const rows = Array.from($tbody.find('tr'))
            .sort((rowA, rowB) => {
                const valueA = $(rowA).find('td').eq(index).text();
                const valueB = $(rowB).find('td').eq(index).text();

                if (currentSort === 'asc') {
                    // Reverse
                    return valueA < valueB;
                } else {
                    return valueA > valueB;
                }
            })
            .map(row => row.outerHTML)
            .join('');
        $tbody.html(rows);
    })

    /**
     * Load a resource when clicking a table row (if the row contains
     * `data-href` attribute).
     */
    .on('click', 'tbody > tr[data-href]', function(e) {
        getResource($(this).data('href'));
    });
	
	
	
	/**
     * Formats a title value by uppercasing the first letter and replacing
     * underscores with spaces.
     */
    function formatTitle(title) {
		var title = title.replace(/[^\w\s]/gi, '')
        return title.slice(0, 1).toUpperCase() + title.slice(1).replace(/_/g, ' ');
    }
	
	
	/**
     * Handles Ajax errors.
     */
    function handleAjaxError(jqXHR) {
        // Status codes 201 and 204 are OK, but as the responses contain no
        // data, jQuery thinks that such Ajax requests fail. Thus, we do here
        // what we do to all other non-failing requests (= call `renderData`).
        if (jqXHR.status === 201 || jqXHR.status === 204) {
            renderData(null);
            return;
        }
		console.log(jqXHR)
        $controlsData.html('');
        $contentData.html(buildError(jqXHR));
    }
	
	/**
     * Will fetch the specific API resource using ajax functionalities.
     */
	 
    function getResource(resource = getCurrentHash(), method = 'GET', data = null) {
		
        if (resource.trim() === '') {
            window.location.hash = apiRoot;
            window.location.reload();
			resource = apiRoot;
        }

        // Adding '/' to the resource if missing
        if (resource.substring(0, 1) !== '/') {
            resource = '/' + resource;
        }

        let url = apiU + resource;
		
		if( method === 'DELETE' ){
			if (resource.substring(0, 1) == '/') {
				resource = resource.substring(1);
			}
			url = resource;
		}
		
		if( method === 'PUT' ){		
			
			if (resource.substr(resource.length - 2) == '//') {
				resource = resource.substring(0, resource.length - 1);
			}
			if (resource.substring(0, 1) == '/') {
				resource = resource.substring(1);
			}
			url = resource;
			console.log(url)
		}
		
        //history.replaceState(null, null, '#!' + resource);

        $.ajax({
            contentType: data !== null ? PLAINJSON : null,
            data: data,
            timeout: xhrTimeout,
            type: method,
            url: url,
        })
        .done(renderData)
        .fail(handleAjaxError)
		
    }
	
	/**
     * Render data returned by AJAX calls.
     */
	function renderData(data) {
        cachedData = data;
		let self_links;
		console.log(data)
		
		try{
			self_links = apiUrl + data["_links"]['add'].href;
		}catch(e){
			//getResource( getCurrentHash() );
			return;
		}
		
		var title = getCurrentHash();

        if (!data) {
            $contentData.html(`
                    <h4>Operation succeeded</h4>
                    <p>${createLink('', 'Reload client')}</p>
                `);
            $controlsData.html('');
            return;
        }
		var html = `<h3>${ formatTitle(title) }</h3>`;
		
		html += `<table><thead><tr> <th>Title</th> <th>Edit</th> <th>Delete</th> </tr></thead><tbody>`;
		
		html += createItems(data['items']);
		
		html += `</tbody></table>`;
		
		html += `<br /> <button class="add-resource btn waves-effect waves-light" type="submit" data-href="${ self_links }" data-href="POST" name="action">Add new
					<i class="material-icons right">add</i>
				  </button>`;
		$controlsData.html(" ");
        $controlsData.html( html );
		$formData.html(" ");

        if (Object.keys(data).length === 2) {
            $contentData.html(buildCollectionTable(data));
        } else {
            $contentData.html(buildSingleTable(data));
        }
    }
	
	function getCurrentHash(){
		return window.location.hash.replace(/^#!?/, '');
	}
	
	/**
     * Build a resource link (i.e. that has class `resource-link`).
     */
    function createLink(href, title, method = 'GET', schemaUrl = '') {
        return `
                <a
                    class="resource-link"
                    href="${escapeAttr(href)}"
                    data-method="${escapeAttr(method)}"
                    data-schema-url="${escapeAttr(schemaUrl)}"
                >${escapeHtml(title)}</a>
            `.trim();
    }
	
	/**
     * Escape values being printed as HTML to prevent XSS injections 
     *
     * Arrays are converted such that each element of the array gets escaped
     * individually.
     *
     */
    function escapeHtml(value) {
        if (Array.isArray(value)) {
            return value.map(val => escapeHtml(val));
        }

        if (typeof value !== 'string') {
            return value;
        }

        return value.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
	
	/**
     * Build an error message for cases when an AJAX call fails.
     */
    function buildError(jqXHR) {
        let html, response;
        try {
            response = JSON.parse(jqXHR.responseText);
        } catch (e) {
            html = `<h4>Error: ${escapeHtml(jqXHR.statusText)}</h4>`;

            if (jqXHR.statusText === 'timeout') {
                html += `<p>Please try to ${createLink(getCurrentHash(), 'reload the client')}.</p>`;
            }

            return html;
        }

        if (response['error']) {
            html = `<h4>Error: ${escapeHtml(response['error']['message'])}</h4>`;
            response['error']['messages'].forEach(function(msg) {
                html += `<p>${escapeHtml(msg)}</p>`;
            });
        } else if (response['message']) {
            html = `<h4>Error:</h4><p>${escapeHtml(response['message'])}</p>`;
        } else {
            html = `
                    <h4>Error: Unknown error</h4>
                    <pre>${escapeHtml(JSON.stringify(response))}</pre>
                `;
        }

        return html;
    }
	
	/**
     * Find the representative title for a resource.
     */
	function getTitle(data) {
		var title = "";
		if(data.title){
			title = data.title;
		}else if( data.username ){
			title = data.username;
		}else if( data.message_details ){
			title = data.message_details;
		}else if( data.details ){
			title = data.details;
		}else if( data.fullname ){
			title = data.fullname;
		}
		
		return title;
	}
	
	/**
     * Build a list of control links.
     */
    function createItems(controls) {
        let html = '';
		
		console.log(controls)
		
        for (key in controls) {
            if (key === 'self') {
                continue;
            }

            const control = controls[key];
			
			var title = getTitle(control);
			
			
            const href    = apiUrl + control._links["self"].href;
            //const href    = getCurrentHash() + '/';
            const method  = control.method || 'GET';

            if (key === 'collection') {
                html += `<li>${createLink(href, `Collection: ${href} (${method})`)}</li>`;
                continue;
            }

            // Skip PATCH resources (not implemented)
            if (method === 'PATCH') {
                continue;
            }

            // "Dynamic" URLs, skip other than GETs (not implemented)
            if (control.isHrefTemplate && (method && method !== 'GET')) {
                continue;
            }

            const schemaUrl = apiUrl + control["_links"]["self"].href || '';

				
			html += `<tr> 
						<td>${createLink(
                            href,
                            `${title} (${method})`,
                            method,
                            schemaUrl
                        )}</td> 
						<td>
						${createLink(
                            href,
                            `Edit`,
                            `PUT`,
                            schemaUrl
                        )}
						</td> 
						<td> 
						${createLink(
                            href,
                            `DELETE`,
                            `DELETE`,
                            schemaUrl
                        )}
						</td> 
					</tr>`
        }

        return html;
    }
	
	
	
	/**
     * Escape an attribute enclosed in double quotes.
     */
    function escapeAttr(value) {
        if (typeof value !== 'string') {
            return value;
        }
		
		// If not string then convert double quotes 
        return value.replace(/"/g, '&quot;');
    }
	
	
	
	/**
     * Build a table for a single resource (e.g. a contact).
     */
    function buildSingleTable(data) {
        let html = '<table class="u-full-width"><tbody>';

        for (key in data) {
            if (key === '@controls') {
                continue;
            }

            html += `
                    <tr>
                        <th>${escapeHtml(formatTitle(key))}</th>
                        <td>${formatTableValue(escapeHtml(data[key]))}</td>
                    </tr>
                `;
        }

        html += '</tbody></table>';
        return html;
    }
	
	 
	/**
     * Formats a value being printed to a table.
     *
     * Nulls get enclosed in `<code>` tags for visual sexiness.
     *
     * Arrays get joined with a comma plus a space.
     *
     * Other values are left intact.
     */
    function formatTableValue(value) {
        if (value === null) {
            return '<code>null</code>';
        } else if (Array.isArray(value)) {
            return value.join(', ');
        } else {
            return value;
        }
    }
	
	
	
	
	
});


	