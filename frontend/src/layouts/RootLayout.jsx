import { Outlet } from 'react-router-dom'

const RootLayout = () => {
    return (
        <div>
            <div>Root Layout</div>
            <Outlet />
        </div>
    )
}

export default RootLayout