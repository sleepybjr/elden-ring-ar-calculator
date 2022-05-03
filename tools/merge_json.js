/*
Run using "node merge_json.js" from the tools directory. Move JSON files from tools/gather_data/output prior to running this.
*/

const Weapon_Reqs_Data = require('../src/json/weapons/weapon_reqs');
const Weapon_Damage = require('../src/json/weapons/weapon_damage');
const Weapon_Scaling = require('../src/json/weapons/weapon_scaling');
const Calc_Correct_Id = require('../src/json/calc_correct_id');
const Weapon_Passive = require('../src/json/weapons/weapon_passive');

const merged_weapons = Weapon_Damage.map(x => Object.assign(x, Weapon_Reqs_Data.find(y => y.fullweaponname.toUpperCase() === x.name.toUpperCase())));
const merged_weapons_scaling = Weapon_Scaling.map(x => Object.assign(x, merged_weapons.find(y => y.fullweaponname.toUpperCase() === x.name.toUpperCase())));
const merged_weapons_all = Calc_Correct_Id.map(x => Object.assign(x, merged_weapons_scaling.find(y => y.fullweaponname.toUpperCase() === x.name.toUpperCase())));
const merged_weapons_all_w_passive = Weapon_Passive.map(x => Object.assign(x, merged_weapons_all.find(y => y.fullweaponname.toUpperCase() === x.name.toUpperCase())));

// console.log(merged_weapons_all_w_passive);

const string_data = JSON.stringify(merged_weapons_all_w_passive);

var fs = require('fs');
fs.writeFile("../src/json/weapons/merged_json_data.json", string_data, function(err) {
    if (err) {
        console.log(err);
    }
});