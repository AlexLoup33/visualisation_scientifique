import vtk
from pathlib import Path

def main():
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(Path(__file__).parent.joinpath("head.vti"))
    reader.Update()
    min, max = reader.GetOutput().GetScalarRange()
    model = reader.GetOutputPort()

    filter = vtk.vtkContourFilter()
    filter.SetNumberOfContours(1)
    filter.SetValue(0, 50)
    filter.SetInputConnection(model)

    lut = vtk.vtkLookupTable()
    lut.SetNumberOfColors(256)
    lut.SetTableRange(min, max)
    lut.SetHueRange(0.0, 0.6)
    lut.Build()

    scalar_bar = vtk.vtkScalarBarActor()
    scalar_bar.SetLookupTable(lut)
    scalar_bar.SetTitle("head value")
    scalar_bar.SetOrientationToVertical()

    slider = vtk.vtkSliderRepresentation2D()
    slider.SetMinimumValue(min)
    slider.SetMaximumValue(max)
    slider.SetValue(filter.GetValue(1))
    slider.SetTitleText("Countour Value")

    slider.GetPoint1Coordinate().SetCoordinateSystemToNormalizedViewport()
    slider.GetPoint1Coordinate().SetValue(0.05, 0.15)

    slider.GetPoint2Coordinate().SetCoordinateSystemToNormalizedViewport()
    slider.GetPoint2Coordinate().SetValue(0.3, 0.15)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(filter.GetOutputPort())
    
    mapper.SetLookupTable(lut)
    mapper.SetUseLookupTableScalarRange(1)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    window = vtk.vtkRenderWindow()
    window.SetSize(1000, 1000)

    interactor = vtk.vtkRenderWindowInteractor()
    
    interactor.SetRenderWindow(window)
    
    renderer = vtk.vtkRenderer()
    window.AddRenderer(renderer)

    renderer.AddActor(actor)
    renderer.AddActor(scalar_bar)

    renderer.SetBackground(0, 0, 0)
    
    def callback(obj, event):
        val = obj.GetRepresentation().GetValue()

        filter.SetValue(0, val)

    slider_widget = vtk.vtkSliderWidget()
    slider_widget.SetInteractor(interactor)
    slider_widget.SetRepresentation(slider)
    slider_widget.On()

    slider_widget.AddObserver("InteractionEvent", callback)

    interactor.Initialize()
    interactor.Start()

if __name__ == "__main__":
    main()