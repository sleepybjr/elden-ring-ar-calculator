import { useState, useMemo, useEffect } from "react";

const DarkModeToggle = () => {
    const [isDark, setIsDark] = useState(true);

    useEffect(() => {
        const prefersDark = window.matchMedia(
          "(prefers-color-scheme: dark)"
        ).matches;
      
        if (prefersDark) {
          setIsDark(true);
        }
      }, []);

    const value = useMemo(() => isDark === undefined ? false : isDark, [isDark])
    useEffect(() => {
        if (value) {
            document.body.classList.add('dark');
            document.querySelectorAll('button').forEach((value) => value.classList.add('dark'));
        } else {
            document.body.classList.remove('dark');
            document.querySelectorAll('button').forEach((value) => value.classList.remove('dark'));
        }
    }, [value]);

    return (
        <input
            type="checkbox"
            className="dark-mode-toggle"
            checked={isDark}
            onChange={({ target }) => setIsDark(target.checked)}
            aria-label="Dark mode toggle"
        />
    );
};

export default DarkModeToggle;