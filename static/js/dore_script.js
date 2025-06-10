$.dore = function (element, options) {

    let defaults = {};
    let plugin = this;
    plugin.settings = {};

    function init() {

        options = options || {};
        plugin.settings = $.extend({}, defaults, options);

        /* 03.02. Resize */
        var subHiddenBreakpoint = 1440;
        var searchHiddenBreakpoint = 768;
        var menuHiddenBreakpoint = 768;

        function onResize() {
            var windowHeight = $(window).outerHeight();
            var windowWidth = $(window).outerWidth();
            var navbarHeight = $(".navbar").outerHeight();

            var submenuMargin = parseInt(
                $(".sub-menu .scroll").css("margin-top"),
                10
            );

            if ($(".chat-app .scroll").length > 0 && chatAppScroll) {
                $(".chat-app .scroll").scrollTop(
                    $(".chat-app .scroll").prop("scrollHeight")
                );
                chatAppScroll.update();
            }

            if (windowWidth < menuHiddenBreakpoint) {
                $("#app-container").addClass("menu-mobile");
            } else if (windowWidth < subHiddenBreakpoint) {
                $("#app-container").removeClass("menu-mobile");
                if ($("#app-container").hasClass("menu-default")) {
                    $("#app-container").removeClass(allMenuClassNames);
                    $("#app-container").addClass("menu-default menu-sub-hidden");
                }
            } else {
                $("#app-container").removeClass("menu-mobile");
                if (
                    $("#app-container").hasClass("menu-default") &&
                    $("#app-container").hasClass("menu-sub-hidden")
                ) {
                    $("#app-container").removeClass("menu-sub-hidden");
                }
            }

            setMenuClassNames(0, true);
        }

        function setDirection() {
            if (typeof Storage !== "undefined") {
                if (localStorage.getItem("dore-direction")) {
                    direction = localStorage.getItem("dore-direction");
                }
                isRtl = direction == "rtl" && true;
            }
        }

        $(window).on("resize", function (event) {
            if (event.originalEvent.isTrusted) {
                onResize();
            }
        });
        onResize();


        /* 03.31. Full Screen */
        function isFullScreen() {
            return (document.fullscreenElement && true) || (document.webkitFullscreenElement && true) || (document.mozFullScreenElement && true) || (document.msFullscreenElement && true);

        }

        function fullscreen() {
            let isInFullScreen = isFullScreen();

            let docElm = document.documentElement;
            if (!isInFullScreen) {
                if (docElm.requestFullscreen) {
                    docElm.requestFullscreen();
                } else if (docElm.mozRequestFullScreen) {
                    docElm.mozRequestFullScreen();
                } else if (docElm.webkitRequestFullScreen) {
                    docElm.webkitRequestFullScreen();
                } else if (docElm.msRequestFullscreen) {
                    docElm.msRequestFullscreen();
                }
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
            }
        }

        $("#fullScreenButton").on("click", function (event) {
            event.preventDefault();
            if (isFullScreen()) {
                $($(this).find("i")[1]).css("display", "none");
                $($(this).find("i")[0]).css("display", "inline");
            } else {
                $($(this).find("i")[1]).css("display", "inline");
                $($(this).find("i")[0]).css("display", "none");
            }
            fullscreen();
        });


        /* 03.05. Menu */
        var menuClickCount = 0;
        var allMenuClassNames = "menu-default menu-hidden sub-hidden main-hidden menu-sub-hidden main-show-temporary sub-show-temporary menu-mobile";

        function setMenuClassNames(clickIndex, calledFromResize, link) {
            menuClickCount = clickIndex;
            var container = $("#app-container");
            if (container.length == 0) {
                return;
            }

            var link = link || getActiveMainMenuLink();

            //menu-default no subpage
            if (
                $(".sub-menu ul[data-link='" + link + "']").length == 0 &&
                (menuClickCount == 2 || calledFromResize)
            ) {
                if ($(window).outerWidth() >= menuHiddenBreakpoint) {
                    if (isClassIncludedApp("menu-default")) {
                        if (calledFromResize) {
                            $("#app-container").removeClass(allMenuClassNames);
                            $("#app-container").addClass("menu-default menu-sub-hidden sub-hidden");
                            menuClickCount = 0; // This one should be changed from 1 to 0
                        } else {
                            $("#app-container").removeClass(allMenuClassNames);
                            $("#app-container").addClass("menu-default main-hidden menu-sub-hidden sub-hidden");
                            menuClickCount = 0;
                        }
                        resizeCarousel();
                        return;
                    }
                }
            }

            //menu-sub-hidden no subpage
            if (
                $(".sub-menu ul[data-link='" + link + "']").length == 0 &&
                (menuClickCount == 1 || calledFromResize)
            ) {
                if ($(window).outerWidth() >= menuHiddenBreakpoint) {
                    if (isClassIncludedApp("menu-sub-hidden")) {
                        if (calledFromResize) {
                            $("#app-container").removeClass(allMenuClassNames);
                            $("#app-container").addClass("menu-sub-hidden sub-hidden");
                            menuClickCount = 0;
                        } else {
                            $("#app-container").removeClass(allMenuClassNames);
                            $("#app-container").addClass("menu-sub-hidden main-hidden sub-hidden");
                            menuClickCount = -1;
                        }
                        resizeCarousel();
                        return;
                    }
                }
            }

            //menu-hidden no subpage
            if (
                $(".sub-menu ul[data-link='" + link + "']").length == 0 &&
                (menuClickCount == 1 || calledFromResize)
            ) {
                if ($(window).outerWidth() >= menuHiddenBreakpoint) {
                    if (isClassIncludedApp("menu-hidden")) {
                        if (calledFromResize) {
                            $("#app-container").removeClass(allMenuClassNames);
                            $("#app-container").addClass("menu-hidden main-hidden sub-hidden");
                            menuClickCount = 0;
                        } else {
                            $("#app-container").removeClass(allMenuClassNames);
                            $("#app-container").addClass("menu-hidden main-show-temporary");
                            menuClickCount = 3;
                        }
                        resizeCarousel();
                        return;
                    }
                }
            }

            let nextClasses = "";
            if (clickIndex % 4 == 0) {
                if (isClassIncludedApp("menu-main-hidden")) {
                    nextClasses = "menu-main-hidden";
                } else if (
                    isClassIncludedApp("menu-default") &&
                    isClassIncludedApp("menu-sub-hidden")
                ) {
                    nextClasses = "menu-default menu-sub-hidden";
                } else if (isClassIncludedApp("menu-default")) {
                    nextClasses = "menu-default";
                } else if (isClassIncludedApp("menu-sub-hidden")) {
                    nextClasses = "menu-sub-hidden";
                } else if (isClassIncludedApp("menu-hidden")) {
                    nextClasses = "menu-hidden";
                }
                menuClickCount = 0;
            } else if (clickIndex % 4 == 1) {
                if (
                    isClassIncludedApp("menu-default") &&
                    isClassIncludedApp("menu-sub-hidden")
                ) {
                    nextClasses = "menu-default menu-sub-hidden main-hidden sub-hidden";
                } else if (isClassIncludedApp("menu-default")) {
                    nextClasses = "menu-default sub-hidden";
                } else if (isClassIncludedApp("menu-main-hidden")) {
                    nextClasses = "menu-main-hidden menu-hidden";
                } else if (isClassIncludedApp("menu-sub-hidden")) {
                    nextClasses = "menu-sub-hidden main-hidden sub-hidden";
                } else if (isClassIncludedApp("menu-hidden")) {
                    nextClasses = "menu-hidden main-show-temporary";
                }
            } else if (clickIndex % 4 == 2) {
                if (isClassIncludedApp("menu-main-hidden") && isClassIncludedApp("menu-hidden")) {
                    nextClasses = "menu-main-hidden";
                } else if (
                    isClassIncludedApp("menu-default") &&
                    isClassIncludedApp("menu-sub-hidden")
                ) {
                    nextClasses = "menu-default menu-sub-hidden sub-hidden";
                } else if (isClassIncludedApp("menu-default")) {
                    nextClasses = "menu-default main-hidden sub-hidden";
                } else if (isClassIncludedApp("menu-sub-hidden")) {
                    nextClasses = "menu-sub-hidden sub-hidden";
                } else if (isClassIncludedApp("menu-hidden")) {
                    nextClasses = "menu-hidden main-show-temporary sub-show-temporary";
                }
            } else if (clickIndex % 4 == 3) {
                if (isClassIncludedApp("menu-main-hidden")) {
                    nextClasses = "menu-main-hidden menu-hidden";
                } else if (
                    isClassIncludedApp("menu-default") &&
                    isClassIncludedApp("menu-sub-hidden")
                ) {
                    nextClasses = "menu-default menu-sub-hidden sub-show-temporary";
                } else if (isClassIncludedApp("menu-default")) {
                    nextClasses = "menu-default sub-hidden";
                } else if (isClassIncludedApp("menu-sub-hidden")) {
                    nextClasses = "menu-sub-hidden sub-show-temporary";
                } else if (isClassIncludedApp("menu-hidden")) {
                    nextClasses = "menu-hidden main-show-temporary";
                }
            }
            if (isClassIncludedApp("menu-mobile")) {
                nextClasses += " menu-mobile";
            }
            container.removeClass(allMenuClassNames);
            container.addClass(nextClasses);
            resizeCarousel();
        }

        $(".menu-button").on("click", function (event) {
            event.preventDefault();
            // event.stopPropagation();
            setMenuClassNames(++menuClickCount);
        });

        $(".menu-button-mobile").on("click", function (event) {
            event.preventDefault();
            // event.stopPropagation();
            $("#app-container")
                .removeClass("sub-show-temporary")
                .toggleClass("main-show-temporary");
            return false;
        });

        $(".main-menu").on("click", "a", function (event) {
            event.preventDefault();
            // event.stopPropagation();
            var link = $(this)
                .attr("href")
                .replace("#", "");
            if ($(".sub-menu ul[data-link='" + link + "']").length == 0) {
                var target = $(this).attr("target");
                if ($(this).attr("target") == null) {
                    window.open(link, "_self");
                } else {
                    window.open(link, target);
                }
                return;
            }

            showSubMenu($(this).attr("href"));
            var container = $("#app-container");
            if (!$("#app-container").hasClass("menu-mobile")) {
                if (
                    $("#app-container").hasClass("menu-sub-hidden") &&
                    (menuClickCount == 2 || menuClickCount == 0)
                ) {
                    setMenuClassNames(3, false, link);
                } else if (
                    $("#app-container").hasClass("menu-hidden") &&
                    (menuClickCount == 1 || menuClickCount == 3)
                ) {
                    setMenuClassNames(2, false, link);
                } else if (
                    $("#app-container").hasClass("menu-default") &&
                    !$("#app-container").hasClass("menu-sub-hidden") &&
                    (menuClickCount == 1 || menuClickCount == 3)
                ) {
                    setMenuClassNames(0, false, link);
                }
            } else {
                $("#app-container").addClass("sub-show-temporary");
            }
            return false;
        });

        $(document).on("click", function (event) {
            if (
                !(
                    $(event.target)
                        .parents()
                        .hasClass("menu-button") ||
                    $(event.target).hasClass("menu-button") ||
                    $(event.target)
                        .parents()
                        //   .hasClass("menu-button-mobile") ||
                        // $(event.target).hasClass("menu-button-mobile") ||
                        // $(event.target)
                        //   .parents()
                        .hasClass("sidebar") ||
                    $(event.target).hasClass("sidebar")
                )
            ) {
                // Prevent sub menu closing on collapse click
                if ($(event.target).parents("a[data-toggle='collapse']").length > 0 || $(event.target).attr("data-toggle") == 'collapse') {
                    return;
                }
                if (
                    $("#app-container").hasClass("menu-sub-hidden") &&
                    menuClickCount == 3
                ) {
                    var link = getActiveMainMenuLink();
                    if (link == lastActiveSubmenu) {
                        setMenuClassNames(2);
                    } else {
                        setMenuClassNames(0);
                    }
                } else if ($("#app-container").hasClass("menu-main-hidden") && $("#app-container").hasClass("menu-mobile")) {
                    setMenuClassNames(0);
                } else if (
                    $("#app-container").hasClass("menu-hidden") ||
                    $("#app-container").hasClass("menu-mobile")
                ) {
                    setMenuClassNames(0);
                }
            }
        });

        function getActiveMainMenuLink() {
            var dataLink = $(".main-menu ul li.active a").attr("href");
            return dataLink ? dataLink.replace("#", "") : "";
        }

        function isClassIncludedApp(className) {
            const container = $("#app-container");
            const classAttr = container.attr("class") || "";
            const classList = classAttr.trim().split(/\s+/);
            return classList.includes(className);
        }

        var lastActiveSubmenu = "";

        function showSubMenu(dataLink) {
            if ($(".main-menu").length == 0) {
                return;
            }

            var link = dataLink ? dataLink.replace("#", "") : "";
            if ($(".sub-menu ul[data-link='" + link + "']").length == 0) {
                $("#app-container").removeClass("sub-show-temporary");

                if ($("#app-container").length == 0) {
                    return;
                }

                if (
                    isClassIncludedApp("menu-sub-hidden") ||
                    isClassIncludedApp("menu-hidden")
                ) {
                    menuClickCount = 0;
                } else {
                    menuClickCount = 1;
                }
                $("#app-container").addClass("sub-hidden");
                noTransition();
                return;
            }
            if (link == lastActiveSubmenu) {
                return;
            }
            $(".sub-menu ul").fadeOut(0);
            $(".sub-menu ul[data-link='" + link + "']").slideDown(100);

            $(".sub-menu .scroll").scrollTop(0);
            lastActiveSubmenu = link;
        }

        function noTransition() {
            $(".sub-menu").addClass("no-transition");
            $("main").addClass("no-transition");
            setTimeout(function () {
                $(".sub-menu").removeClass("no-transition");
                $("main").removeClass("no-transition");
            }, 350);
        }

        showSubMenu($(".main-menu ul li.active a").attr("href"));

        function resizeCarousel() {
            setTimeout(() => {
                window.dispatchEvent(new Event("resize"));
            }, 350);
        }


        /* 03.33. Showing Body */
        $("body > *").css({opacity: 0});

        setTimeout(function () {
            $("body").removeClass("show-spinner");
            $("main").addClass("default-transition");
            $(".sub-menu").addClass("default-transition");
            $(".main-menu").addClass("default-transition");
            $(".theme-colors").addClass("default-transition");
            $("body > *").animate({opacity: 1}, 100);
        }, 300);


    }

    init();
};

$.fn.dore = function (options) {
    return this.each(function () {
        if (undefined == $(this).data("dore")) {
            let plugin = new $.dore(this, options);
            $(this).data("dore", plugin);
        }
    });
};