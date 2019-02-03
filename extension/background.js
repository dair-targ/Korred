const extractValue = async (key, rule, tabId) => {
    const results = await browser.tabs.executeScript(
        tabId,
        {code: `document.querySelector("${rule.selector}").innerText`}
    );
    return {[key]: (results.length < 1) ? undefined : results[0]};
};


const extractValues = async (rules, tabId) =>
    Object.assign({}, ...Promise.all(Object.keys(rules).map(key => extractValue(key, rules[key], tabId))));


browser.browserAction.onClicked.addListener(async (tab) => {
    try {
        // Get config
        const config = (await browser.runtime.sendNativeMessage('korred', {type: "config"})).output;
        // Extract values from the opened tab
        const envValues = config.env ? await extractValues(config.env, tab.id) : {};
        const argsValues = config.args ? Object.values(await extractValues(config.args, tab.id)) : [];
        // Request native app to run a script using extracted values
        const response = await browser.runtime.sendNativeMessage(
            'korred',
            {type: "run", env: envValues, args: argsValues},
        );
        console.log(response);
    } catch (e) {
        console.error(e);
    }
});
