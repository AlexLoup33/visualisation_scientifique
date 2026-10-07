import vtk
from pathlib import Path

def main():
    #Loading the dataset head.vti
    reader = vtk.vtkXMLImageDataReader() # Reader Object
    reader.SetFileName(Path(__file__).parent.joinpath("head.vti")) # Path to the dataset
    reader.Update()
    min, max = reader.GetOutput().GetScalarRange()
    model = reader.GetOutputPort()

    filter = vtk.vtkContourFilter()
    filter.SetNumberOfContours(1)
    filter.SetValue(0, 50)
    filter.SetInputConnection(model)

    # LookUp Table
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfColors(256)
    lut.SetTableRange(min, max)
    lut.SetHueRange(0.0, 0.6)
    lut.Build()

    # Head Scalar
    scalar_bar = vtk.vtkScalarBarActor()
    scalar_bar.SetLookupTable(lut)
    scalar_bar.SetTitle("Head")
    scalar_bar.SetOrientationToVertical()

    # Slider
    slider = vtk.vtkSliderRepresentation2D()
    slider.SetMinimumValue(min)
    slider.SetMaximumValue(max)
    slider.SetValue(20)
    slider.SetTitleText("Countour Value")
    
    slider.SetSliderWidth(0.5)

    slider.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    slider.GetPoint1Coordinate().SetValue(0.1, 0.1)

    slider.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    slider.GetPoint2Coordinate().SetValue(0.1, 0.3)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(filter.GetOutputPort())
    
    # Link the LookUp Table with mapper
    mapper.SetLookupTable(lut)
    mapper.SetUseLookupTableScalarRange(1)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    window = vtk.vtkRenderWindow()
    window.SetSize(1000, 1000)

    interactor = vtk.vtkRenderWindowInteractor()
    
    #WIDGETS
    slider_widget = vtk.vtkSliderWidget()
    slider_widget.SetInteractor(interactor)
    slider_widget.SetRepresentation(slider)
    slider_widget.On()
    
    interactor.SetRenderWindow(window)
    
    renderer = vtk.vtkRenderer()
    window.AddRenderer(renderer)

    renderer.AddActor(actor)
    renderer.AddActor(scalar_bar)

    renderer.SetBackground(0.1, 0.1, 0.4)

    interactor.Initialize()
    interactor.Start()

if __name__ == "__main__":
    main()