const menuItemId = 'open-ssh-to';
browser.contextMenus.create({
    id: menuItemId,
    title: 'Open SSH to...',
    contexts: ['selection']
});
browser.contextMenus.onClicked.addListener(async (info, tab) => {
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
