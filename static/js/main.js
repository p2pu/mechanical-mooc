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

            $('.navbar-btn').sidr({
                name: 'main-menu-panel',
                source: '.nav-collapse.collapse'
            });
        });
    },
        timezoneDetectionHandler = function () {
            var timezone = jstz.determine();
            $("#timezone").val(timezone.name());
            $("#timezoneHelp").append("We've pre-selected <span class=\"label label-info\">" + timezone.name() + "</span> using your clock.");
        },
        countrySelectHandler = function () {
            var idCountrySelect = $("#id_country_select");
            idCountrySelect.prop("selectedIndex", -1);
            idCountrySelect.change(function () {
                if ($('#id_country_select').val() === 'United States') {
                    $('#id_state_input').show();
                } else {
                    $('#id_state_input').hide();
                }
                $("#id_state_select").prop("selectedIndex", -1);
            });
        },
        emailValidationHandler = function () {
            $("#emailForm").validate({
                debug: true,
                rules: {
                    email: {
                        required: true,
                        email: true
                    }
                },
                errorClass: "error",
                highlight: function (element, errorClass) {
                    $("#emailForm .control-group").addClass(errorClass);
                },
                unhighlight: function (element, errorClass, validClass) {
                    $("#emailForm .control-group").removeClass(errorClass);
                },
                errorPlacement: function (error, element) {
                    $("#emailForm .control-group").prepend(error);
                },
                submitHandler: function (form) {
                    $("#hiddenEmailField").val($("#email").val());
                    $("#step1").hide("slide", { direction: "left" }, 500, function () {
                        $("#step2").show("slide", { direction: "right" }, 500);
                    });
                }
            });
        },
        infoFormValidationHandler = function () {
            $("#infoForm").validate({
                debug: true,
                rules: {
                    username: "required",
                    educationrole: "required",
                    country: "required",
                    us_state: {
                        required: {
                            depends: function () {
                                return $('#id_country_select').val() == 'United States';
                            }
                        }
                    },
                    timezone: "required",
                },
                errorClass: "error",
                highlight: function (element, errorClass) {
                    $(element).parents(".control-group").addClass(errorClass);
                },
                unhighlight: function (element, errorClass, validClass) {
                    $(element).parents(".control-group").removeClass(errorClass);
                },
                errorPlacement: function () {
                },
                submitHandler: function (form) {
                    form.submit();
                }
            });
        },
        signup = function () {

            $(function () {
                emailValidationHandler();
                timezoneDetectionHandler();
                countrySelectHandler();
                infoFormValidationHandler();
            });
        };

    MMOOC.Splash = {};
    MMOOC.Splash.init = init;
    MMOOC.Splash.signup = signup;

}(jQuery, MMOOC));