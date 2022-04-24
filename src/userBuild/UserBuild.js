import { handleWeaponRight1Change } from '../weapons/userBuildSlice';// eslint-disable-line no-unused-vars
import { useSelector, useDispatch } from 'react-redux';// eslint-disable-line no-unused-vars

export default function UserBuild() {
    const weaponLeft1 = useSelector((state) => state.userBuild.weaponLeft1);
    const weaponLeft2 = useSelector((state) => state.userBuild.weaponLeft2);
    const weaponLeft3 = useSelector((state) => state.userBuild.weaponLeft3);
    const weaponRight1 = useSelector((state) => state.userBuild.weaponRight1);
    const weaponRight2 = useSelector((state) => state.userBuild.weaponRight2);
    const weaponRight3 = useSelector((state) => state.userBuild.weaponRight3);

    return (
        <div className='extra-spacing'>
            <div>
                Weapon Left 1: {weaponLeft1.name}
                <br />
                Weapon Left 2: {weaponLeft2.name}
                <br />
                {/* levels aren't calculated anymore after copy */}
                Weapon Left 3: {weaponLeft3.name} {weaponLeft3.final_physical}
                <br />
            </div>
            <div>
                Weapon Right 1: {weaponRight1.name}
                <br />
                Weapon Right 2: {weaponRight2.name}
                <br />
                Weapon Right 3: {weaponRight3.name}
                <br />
            </div>
            <div>
                Helmet:
                <br />
                Chest:
                <br />
                Gauntlets:
                <br />
                Shoes:
                <br />
            </div>
            <div>
                Current Load:
                <br />
                Maximum Load:
            </div>
        </div>
    );
}