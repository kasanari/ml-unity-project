using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class RollerAcademy : Academy
{

    public CameraController mainCamera;

    public override void InitializeAcademy()
    {
        mainCamera.ResetCamera();
    }

    public override void AcademyReset()
    {
        mainCamera.ResetCamera();
    }


}
