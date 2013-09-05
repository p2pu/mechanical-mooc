/*global jQuery, window, document, console, OpenBadges */

var MMOOC = window.MMOOC || {};

(function ($, MMOOC) {
    'use strict';

    var init = function () {
        $(function () {

            $('.navbar-btn').sidr({
                name: 'main-menu-panel',
                source: '.nav-collapse.collapse'
            });
        });
    }

    , timezone_detection_handler = function () {
        var timezone = jstz.determine();
        $("#timezone").val(timezone.name());
    }

    , country_select_handler = function () {
        $("#id_country_select").prop("selectedIndex", -1);
        $("#id_country_select").change(function () {
            if ($('#id_country_select').val() == 'United States') {
                $('#id_state_input').show();
            } else {
                $('#id_state_input').hide();
            }
            $("#id_state_select").prop("selectedIndex", -1);
        });
    }

    , email_validation_handler = function () {
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
    }

    ,info_form_validation_handler = function () {
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
    }

    , signup = function () {

        $(function () {
            email_validation_handler();
            timezone_detection_handler();
            country_select_handler();
            info_form_validation_handler();
        });
    }

    MMOOC.Splash = {};
    MMOOC.Splash.init = init;
    MMOOC.Splash.signup = signup;

}(jQuery, MMOOC));