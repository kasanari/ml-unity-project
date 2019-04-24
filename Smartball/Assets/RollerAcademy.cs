using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class RollerAcademy : Academy
{
    public Transform Target;
    public Rigidbody Sphere;
    public List<Vector3> spawn_points = new List<Vector3>();
    public CameraController mainCamera;


    public void SetSpawnPositions()
    {
        Random random = new Random();
        Vector3 start_point = new Vector3(-17.5f, 0.5f, -17.5f);

        //int target_spawn_offset_x = Random.Range(0, 35);
        //int target_spawn_offset_z = Random.Range(0, 35);
        /* int sphere_spawn_index = Random.Range(0, spawn_points.Count);

         while (target_spawn_index == sphere_spawn_index)
         {
             sphere_spawn_index = Random.Range(0, spawn_points.Count);
         }*/




        Target.position = start_point + (new Vector3(Random.Range(0, 7)*5, 0, Random.Range(0, 7)*5));
        print("Set goal at: " + Target.position);
        Sphere.position = start_point + (new Vector3(Random.Range(0, 7) * 5, 0, Random.Range(0, 7) * 5));
        Sphere.velocity = Vector3.zero;
        Sphere.angularVelocity = Vector3.zero;
        print("Set agent at: " + Sphere.position);
    }

    public override void InitializeAcademy()
    {
        spawn_points.Add(new Vector3(17f, 0.5f, 17f));
        spawn_points.Add(new Vector3(-17f, 0.5f, 17f));
        spawn_points.Add(new Vector3(17f, 0.5f, -17f));
        spawn_points.Add(new Vector3(-17f, 0.5f, -17f));


        SetSpawnPositions();
        mainCamera.ResetCamera();
    }

    public override void AcademyReset()
    {
        SetSpawnPositions();
        mainCamera.ResetCamera();
    }


}
