import armorOptimizer from './ArmorOptimizer';

// eslint-disable-next-line no-restricted-globals
self.onmessage = ({ data: {
    equippedArmor,
    loadRemaining,
    adjustedResistances,
    resistancesMultiplier,
    currEquippedArmor
} }) => {
    const output = armorOptimizer(equippedArmor, loadRemaining, adjustedResistances, resistancesMultiplier, currEquippedArmor);
    // eslint-disable-next-line no-restricted-globals
    postMessage({
        output: output,
        equippedArmor: currEquippedArmor,
    });
};