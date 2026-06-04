(function () {
    var $ = django.jQuery;
    var DASH_RE = /^-{5,}$/;

    function fixOption(opt) {
        var text = $.trim($(opt).text());
        if (DASH_RE.test(text)) {
            var name = $(opt).closest('select').attr('name') || '';
            $(opt).text(name === 'action' ? 'Select' : 'All');
        }
    }

    function fixSourceOptions() {
        $('select option').each(function () { fixOption(this); });
    }

    function fixRenderedItems() {
        // Fix items inside an open Select2 dropdown
        $('.select2-results__option').each(function () {
            if (DASH_RE.test($.trim($(this).text()))) {
                $(this).text('All');
            }
        });
        // Fix the closed "selected value" display
        $('.select2-selection__rendered').each(function () {
            var title = $(this).attr('title') || '';
            var text  = $.trim($(this).text());
            if (DASH_RE.test(title)) { $(this).attr('title', 'All'); }
            if (DASH_RE.test(text))  { $(this).text('All'); }
        });
    }

    function fullFix() {
        fixSourceOptions();
        fixRenderedItems();
    }

    $(document).ready(function () {
        // Run immediately and after Select2 has had time to initialize
        fullFix();
        setTimeout(fullFix, 200);
        setTimeout(fullFix, 800);

        // Every time any Select2 dropdown opens, fix the rendered list items
        $(document).on('select2:open', function () {
            // give Select2 time to inject the <ul> into the DOM
            setTimeout(fixRenderedItems, 20);
            setTimeout(fixRenderedItems, 100);
        });

        // After selection / close, fix the "selected" display text
        $(document).on('select2:close select2:select select2:unselect', function () {
            setTimeout(fixRenderedItems, 20);
        });

        // Catch any future dynamic selects (e.g. inline formsets)
        var observer = new MutationObserver(function () {
            setTimeout(fixRenderedItems, 50);
        });
        observer.observe(document.body, { childList: true, subtree: true });
    });
})();
