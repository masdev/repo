import { createBrowserRouter, Route, createRoutesFromElements, RouterProvider } from 'react-router-dom'
import RootLayout from './layouts/RootLayout'
import Home from './pages/Home'
import Login from './pages/Login'
import Cars from './pages/Cars'
import SingleCar from './pages/SingleCar'
import NewCar from './pages/NewCar'
import NotFound from './pages/NotFound'
import { carsLoader } from './pages/Cars'

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path='/' element={<RootLayout />}>
      <Route index element={<Home />} />
      <Route path="cars" element={<Cars />} loader={carsLoader} />
      <Route path="login" element={<Login />} />
      <Route path="new-car" element={<NewCar />} />
      <Route path="car/:id" element={<SingleCar />} />
      <Route path="*" element={<NotFound />} />
    </Route>   
  )
)

function App() {
  return (
    <RouterProvider router={router} />
  )
}

export default App
