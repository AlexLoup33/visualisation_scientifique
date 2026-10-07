import vtk
from pathlib import Path

def main():
    # Charger le modèle head.vti
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(Path(__file__).parent.joinpath("head.vti"))
    reader.Update()
    min, max = reader.GetOutput().GetScalarRange() # Récupérer le min et le max du scalaire
    model = reader.GetOutputPort()

    # Filtre Isométrique
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

    # Scalaire de Head
    scalar_bar = vtk.vtkScalarBarActor()
    scalar_bar.SetLookupTable(lut)
    scalar_bar.SetTitle("head value")
    scalar_bar.SetOrientationToVertical()

    # Slider
    slider = vtk.vtkSliderRepresentation2D()
    slider.SetMinimumValue(min)
    slider.SetMaximumValue(max)
    slider.SetValue(filter.GetValue(1))
    slider.SetTitleText("Countour Value")

    slider.GetPoint1Coordinate().SetCoordinateSystemToNormalizedViewport()
    slider.GetPoint1Coordinate().SetValue(0.05, 0.15)

    slider.GetPoint2Coordinate().SetCoordinateSystemToNormalizedViewport()
    slider.GetPoint2Coordinate().SetValue(0.3, 0.15)

    # Chargement du modèle dans le mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(filter.GetOutputPort())
    
    # Lien la LookUp Table avec le mapper
    mapper.SetLookupTable(lut)
    mapper.SetUseLookupTableScalarRange(1)

    # Actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Declaration de la fênetre
    window = vtk.vtkRenderWindow()
    window.SetSize(1000, 1000)

    # Déclaration de l'interactor
    interactor = vtk.vtkRenderWindowInteractor()
    
    interactor.SetRenderWindow(window)
    
    renderer = vtk.vtkRenderer()
    window.AddRenderer(renderer)

    renderer.AddActor(actor)
    renderer.AddActor(scalar_bar)

    renderer.SetBackground(0, 0, 0)
    
    # Callback du slider
    def callback(obj, event):
        #print(f"Interaction {event} attrapé !")
        # Récupère la valeur dans obj (slider)
        val = obj.GetRepresentation().GetValue()

        # L'attribut à attribuer à filter
        filter.SetValue(0, val)

    # Widget du slider
    slider_widget = vtk.vtkSliderWidget()
    slider_widget.SetInteractor(interactor)
    slider_widget.SetRepresentation(slider)
    slider_widget.On()

    slider_widget.AddObserver("InteractionEvent", callback)

    interactor.Initialize()
    interactor.Start()

if __name__ == "__main__":
    main()