// cpp/bindings/simulation_bindings.cpp

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "axabsent/simulation/dynamics.hpp"
#include "axabsent/simulation/quantum.hpp"

namespace py = pybind11;
using namespace axabsent::simulation;

PYBIND11_MODULE(axabsent_core_bindings, m) {
    py::class_<DynamicSimulator>(m, "DynamicSimulator")
        .def(py::init<>())
        .def("initialize", &DynamicSimulator::initialize, "Initialize system with initial states")
        .def("step", &DynamicSimulator::step, "Advance the simulation by one timestep")
        .def("run", &DynamicSimulator::run, py::arg("steps"), "Run simulation for a number of steps")
        .def("get_state", &DynamicSimulator::get_state, "Get current system state")
        .def("reset", &DynamicSimulator::reset, "Reset simulation")
        .def("__repr__", [](const DynamicSimulator&) {
            return "<DynamicSimulator>";
        });

    py::class_<QuantumFieldSimulator>(m, "QuantumFieldSimulator")
        .def(py::init<>())
        .def("configure_grid", &QuantumFieldSimulator::configure_grid, "Configure quantum grid parameters")
        .def("set_initial_conditions", &QuantumFieldSimulator::set_initial_conditions, "Set field initial values")
        .def("evolve", &QuantumFieldSimulator::evolve, "Evolve the quantum field")
        .def("extract_observables", &QuantumFieldSimulator::extract_observables, "Extract measurement data")
        .def("__repr__", [](const QuantumFieldSimulator&) {
            return "<QuantumFieldSimulator>";
        });
}
