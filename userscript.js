// ==UserScript==
// @name         SEC TXT URLs Copier
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Adds a button to copy all .txt filing URLs to clipboard
// @author       Grok
// @match        https://www.sec.gov/cgi-bin/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Create a fixed-position button
    const button = document.createElement('button');
    button.textContent = 'Copy TXT URLs';
    button.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 9999;
        padding: 10px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
    `;
    button.addEventListener('mouseover', () => {
        button.style.backgroundColor = '#0056b3';
    });
    button.addEventListener('mouseout', () => {
        button.style.backgroundColor = '#007bff';
    });

    document.body.appendChild(button);

    // Button click handler
    button.addEventListener('click', () => {
        // Find all <a> elements with href ending in .txt
        const txtLinks = document.querySelectorAll('a[href$=".txt"]');
        const urls = Array.from(txtLinks).map(link => link.href).filter(href => href.endsWith('.txt'));

        if (urls.length === 0) {
            alert('No .txt URLs found on this page.');
            return;
        }

        // Join URLs with newlines for easy pasting
        const textToCopy = urls.join('\n');

        // Copy to clipboard
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                alert(`Copied ${urls.length} TXT URLs to clipboard!`);
            })
            .catch(err => {
                console.error('Failed to copy text: ', err);
                alert('Failed to copy to clipboard. Please check console for errors.');
            });
    });
})();