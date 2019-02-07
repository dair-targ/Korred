const menuItemId = 'open-ssh-to';

browser.menus.create({
    id: menuItemId,
    title: 'Open SSH to...',
    contexts: ['selection']
});

browser.menus.onClicked.addListener(async (
        info: browser.menus.OnClickData,
        tab: browser.tabs.Tab,
) => {
    if (info.menuItemId === menuItemId) {
        await browser.runtime.sendNativeMessage(
            'korred',
            {type: "run", args: [
                "ssh",
                info.selectionText,
            ]},
        );
    }
});
