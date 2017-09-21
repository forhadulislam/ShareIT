/**
 * Formats a title value by uppercasing the first letter and replacing
 * underscores with spaces.
 */
function formatTitle(title) {
    var title = title.replace(/[^\w\s]/gi, '')
    return title.slice(0, 1).toUpperCase() + title.slice(1).replace(/_/g, ' ');
}


// Creates slug from text
function sluggify(str) {
    var pattern = /\s/g;
    return str.replace(pattern, '-').toLowerCase();
}

// Sorts array
function customSort(a,b) {
    return( a.toString().length - b.toString().length );
}

// Gets current hash
function getCurrentHash(){
    return window.location.hash.replace(/^#!?/, '');
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

/*
    Converts timestamp to understandable time format. 
*/
function time(s) {
    return new Date(s * 1e3).toISOString().slice(-13, -5);
}
