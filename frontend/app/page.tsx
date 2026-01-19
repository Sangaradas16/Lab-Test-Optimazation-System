"use client"

import { useState } from "react"
import { Activity, CheckCircle2, Search, TestTube2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { cn } from "@/lib/utils"

// Types matching Backend
interface TestRecommendation {
  test_name: string
  reason: string
  cost: number
  importance: "High" | "Medium" | "Low"
}

interface OptimizationResult {
  recommended_tests: TestRecommendation[]
  predicted_diseases: string[]
  total_cost: number
  savings: number
  confidence_score: number
}

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<OptimizationResult | null>(null)

  // Form State
  const [age, setAge] = useState("")
  const [gender, setGender] = useState("Male")
  const [symptoms, setSymptoms] = useState("")
  const [history, setHistory] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      // Parse symptoms
      const symptomList = symptoms.split(",").map(s => s.trim()).filter(s => s)

      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          age: parseInt(age) || 30,
          gender,
          symptoms: symptomList,
          history
        })
      })

      if (!response.ok) {
        throw new Error("Failed to analyze data")
      }

      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error(error)
      alert("Error connecting to the optimization engine. Ensure backend is running.")
    } finally {
      setLoading(false)
    }
  }

  const resetForm = () => {
    setResult(null)
    setSymptoms("")
    setHistory("")
  }



  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 p-4 md:p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">

        {/* Header */}
        <div className="flex items-center space-x-4 mb-8">
          <div className="p-3 bg-blue-600 rounded-lg shadow-lg">
            <TestTube2 className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-50">
              Lab Test Optimization System
            </h1>
            <p className="text-slate-500 dark:text-slate-400">
              AI-driven diagnostic efficiency and cost reduction
            </p>
          </div>
        </div>

        {!result ? (
          /* Input Section */
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Card className="md:col-span-1 shadow-md border-slate-200">
              <CardHeader>
                <CardTitle>Patient Assessment</CardTitle>
                <CardDescription>Enter patient demographics and clinical signs.</CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="age">Age</Label>
                      <Input id="age" type="number" placeholder="30" value={age} onChange={e => setAge(e.target.value)} required />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="gender">Gender</Label>
                      <select
                        id="gender"
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                        value={gender}
                        onChange={e => setGender(e.target.value)}
                      >
                        <option>Male</option>
                        <option>Female</option>
                        <option>Other</option>
                      </select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="symptoms">Symptoms (comma separated)</Label>
                    <Input
                      id="symptoms"
                      placeholder="e.g. fever, joint pain, fatigue"
                      value={symptoms}
                      onChange={e => setSymptoms(e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="history">Medical History</Label>
                    <Input
                      id="history"
                      placeholder="e.g. diabetes, hypertension"
                      value={history}
                      onChange={e => setHistory(e.target.value)}
                    />
                  </div>

                  <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700" disabled={loading}>
                    {loading ? <Activity className="mr-2 h-4 w-4 animate-spin" /> : <Search className="mr-2 h-4 w-4" />}
                    {loading ? "Analyzing..." : "Analyze & Recommend"}
                  </Button>
                </form>
              </CardContent>
            </Card>

            <Card className="md:col-span-1 bg-gradient-to-br from-blue-50 to-indigo-50 border-none shadow-none flex flex-col justify-center items-center text-center p-8">
              <div className="bg-white p-4 rounded-full shadow-sm mb-4">
                <Activity className="w-12 h-12 text-blue-500" />
              </div>
              <h3 className="text-xl font-semibold text-blue-900 mb-2">Smart Diagnostics</h3>
              <p className="text-blue-700 max-w-xs">
                Our AI engine analyzes symptoms to predict risks and suggest only the most high-impact lab tests.
              </p>
            </Card>
          </div>
        ) : (
          /* Results Section */
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <Button variant="outline" onClick={resetForm} className="mb-4">
              ← New Assessment
            </Button>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Essential Tests Metric */}
              <Card className="bg-white shadow-md border-l-4 border-l-blue-500">
                <CardHeader className="pb-2">
                  <CardTitle className="text-lg flex items-center text-blue-700">
                    <TestTube2 className="w-5 h-5 mr-2" />
                    Essential Tests
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-blue-700">
                    {result.recommended_tests.length} Recommended
                  </div>
                  <p className="text-sm text-blue-600">Prioritized for clinical value</p>
                </CardContent>
              </Card>

              {/* Cost Reduction Metric */}
              <Card className="bg-white shadow-md border-l-4 border-l-green-500">
                <CardHeader className="pb-2">
                  <CardTitle className="text-lg flex items-center text-green-700">
                    <CheckCircle2 className="w-5 h-5 mr-2" />
                    Cost Reduction
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-green-700">
                    {((result.savings / (result.total_cost + result.savings)) * 100).toFixed(0)}%
                  </div>
                  <p className="text-sm text-green-600">Optimized efficiency</p>
                </CardContent>
              </Card>

              {/* Faster Diagnosis Metric */}
              <Card className="bg-white shadow-md border-l-4 border-l-purple-500">
                <CardHeader className="pb-2">
                  <CardTitle className="text-lg flex items-center text-purple-700">
                    <Activity className="w-5 h-5 mr-2" />
                    Faster Diagnosis
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-lg font-bold text-purple-700">
                    Hours vs Days
                  </div>
                  <p className="text-sm text-purple-600">Accelerated insights</p>
                </CardContent>
              </Card>
            </div>

            {/* Recommended Tests List (No Cost) */}
            <Card className="shadow-md">
              <CardHeader>
                <CardTitle>Recommended Diagnostic Tests</CardTitle>
                <CardDescription>Prioritized list based on clinical value.</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {result.recommended_tests.map((test, index) => (
                    <div key={index} className="flex items-start justify-between p-4 rounded-lg border bg-slate-50/50 hover:bg-slate-50 transition-colors">
                      <div>
                        <div className="flex items-center space-x-2">
                          <h4 className="font-semibold text-slate-800">{test.test_name}</h4>
                          <span className={cn(
                            "text-xs px-2 py-0.5 rounded-full font-medium",
                            test.importance === "High" ? "bg-red-100 text-red-700" : "bg-yellow-100 text-yellow-700"
                          )}>
                            {test.importance} Priority
                          </span>
                        </div>
                        {/* Cost hidden as requested */}
                        <p className="text-sm text-slate-600 mt-1">{test.reason}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}
