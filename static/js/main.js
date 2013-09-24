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
    },
        timezoneDetectionHandler = function () {
            var timezone = jstz.determine();
            $("#timezone").val(timezone.name());
            $("#timezoneHelp").append("We've pre-selected <span class=\"label label-info\">" + timezone.name() + "</span> using your clock.");
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
                    criticalListening: "required",
                    editingAndMixing: "required",
                    sharing: "required",
                    artist1: "required",
                    artist2: "required",
                    artist3: "required",
                    artist4: "required",
                    artist5: "required",
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
                infoFormValidationHandler();
            });
        };

    MMOOC.Splash = {};
    MMOOC.Splash.init = init;
    MMOOC.Splash.signup = signup;

}(jQuery, MMOOC));
