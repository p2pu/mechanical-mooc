/*global jQuery, window, document, console, OpenBadges */

var MMOOC = window.MMOOC || {};

(function ($, MMOOC) {
    'use strict';

    var init = function () {
        $(function () {
            $(".p2pu-tab").p2puSlider({
                navbarContainer: '.navbar',
                icon: '.p2pu-tab-icon',
                iconUp: 'icon-chevron-sign-down',
                iconDown: 'icon-chevron-sign-up'
            });
        });
    };

    MMOOC.Splash = {};
    MMOOC.Splash.init = init;

}(jQuery, MMOOC));